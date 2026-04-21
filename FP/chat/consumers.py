import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from datetime import timedelta
from .models import CallLog
from users.models import User

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'call_{self.room_name}'
        self.call_log_id = None
        self.timeout_task = None

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Cancel timeout if exists
        if self.timeout_task and not self.timeout_task.done():
            self.timeout_task.cancel()
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        # Handle different message types
        if message_type == 'call-offer':
            await self.handle_call_offer(data)
        elif message_type == 'call-answer':
            await self.handle_call_answer(data)
        elif message_type == 'call-rejected':
            await self.handle_call_rejected(data)
        elif message_type == 'call-ended':
            await self.handle_call_ended(data)
        elif message_type == 'call-timeout':
            await self.handle_call_timeout(data)
        else:
            # Forward other signaling messages (ICE candidates, etc.)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'call_message',
                    'message': data
                }
            )

    async def handle_call_offer(self, data):
        """Handle incoming call offer and create CallLog entry"""
        caller_id = data.get('from')
        receiver_id = data.get('to')
        call_type = data.get('callType', 'audio')

        # Create CallLog entry
        self.call_log_id = await self.create_call_log(
            caller_id, receiver_id, call_type, 'missed'
        )

        # Start timeout task (30 seconds)
        self.timeout_task = asyncio.create_task(self.call_timeout_handler(30))

        # Forward the offer
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_message',
                'message': data
            }
        )

    async def handle_call_answer(self, data):
        """Handle call answer and update CallLog to completed"""
        # Cancel timeout since call was answered
        if self.timeout_task and not self.timeout_task.done():
            self.timeout_task.cancel()

        # Update CallLog status to completed
        if self.call_log_id:
            await self.update_call_log_status(self.call_log_id, 'completed')

        # Forward the answer
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_message',
                'message': data
            }
        )

    async def handle_call_rejected(self, data):
        """Handle call rejection"""
        # Cancel timeout
        if self.timeout_task and not self.timeout_task.done():
            self.timeout_task.cancel()

        # Update CallLog status to rejected
        if self.call_log_id:
            await self.update_call_log_status(self.call_log_id, 'rejected')

        # Forward the rejection
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_message',
                'message': data
            }
        )

    async def handle_call_ended(self, data):
        """Handle call end and update duration"""
        duration = data.get('duration', 0)
        
        # Update CallLog with duration and end time
        if self.call_log_id:
            await self.update_call_log_end(self.call_log_id, duration)

        # Forward the end message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_message',
                'message': data
            }
        )

    async def handle_call_timeout(self, data):
        """Handle call timeout (missed call)"""
        # Update CallLog status to missed (it's already missed, but ensure it)
        if self.call_log_id:
            await self.update_call_log_status(self.call_log_id, 'missed')

        # Forward timeout message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_message',
                'message': data
            }
        )

    async def call_timeout_handler(self, seconds):
        """Async timeout handler"""
        try:
            await asyncio.sleep(seconds)
            # If we reach here, call wasn't answered
            if self.call_log_id:
                await self.update_call_log_status(self.call_log_id, 'missed')
        except asyncio.CancelledError:
            # Timeout was cancelled (call was answered/rejected)
            pass

    # Receive message from room group
    async def call_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    # Database operations
    @database_sync_to_async
    def create_call_log(self, caller_id, receiver_id, call_type, status):
        """Create a new CallLog entry"""
        try:
            caller = User.objects.get(id=caller_id)
            receiver = User.objects.get(id=receiver_id)
            call_log = CallLog.objects.create(
                caller=caller,
                receiver=receiver,
                call_type=call_type,
                status=status
            )
            return call_log.id
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def update_call_log_status(self, call_log_id, status):
        """Update CallLog status"""
        try:
            call_log = CallLog.objects.get(id=call_log_id)
            call_log.status = status
            call_log.save()
        except CallLog.DoesNotExist:
            pass

    @database_sync_to_async
    def update_call_log_end(self, call_log_id, duration):
        """Update CallLog with end time and duration"""
        try:
            call_log = CallLog.objects.get(id=call_log_id)
            call_log.ended_at = timezone.now()
            call_log.duration = duration
            call_log.save()
        except CallLog.DoesNotExist:
            pass

