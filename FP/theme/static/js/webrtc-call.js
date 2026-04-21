// WebRTC Call Manager
class CallManager {
    constructor(roomName, currentUserId, otherUserId) {
        this.roomName = roomName;
        this.currentUserId = currentUserId;
        this.otherUserId = otherUserId;
        this.peerConnection = null;
        this.localStream = null;
        this.remoteStream = null;
        this.callSocket = null;
        this.callType = null; // 'audio' or 'video'
        this.callStartTime = null;
        this.callTimerInterval = null;
        this.callTimeout = null; // Timeout for unanswered calls
        this.callAnswered = false; // Track if call was answered

        // ICE servers configuration
        this.iceServers = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' }
            ]
        };
    }

    // Initialize WebSocket connection
    initializeWebSocket() {
        // Don't create a new connection if one already exists and is open
        if (this.callSocket && (this.callSocket.readyState === WebSocket.OPEN || this.callSocket.readyState === WebSocket.CONNECTING)) {
            console.log('WebSocket already exists and is open/connecting');
            return;
        }

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/call/${this.roomName}/`;

        console.log('Initializing WebSocket connection to:', wsUrl);
        this.callSocket = new WebSocket(wsUrl);

        this.callSocket.onopen = () => {
            console.log('WebSocket connection established');
        };

        this.callSocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleSignalingMessage(data);
        };

        this.callSocket.onclose = () => {
            console.log('WebSocket closed');
        };

        this.callSocket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    // Handle incoming signaling messages
    async handleSignalingMessage(data) {
        switch (data.type) {
            case 'call-offer':
                await this.handleCallOffer(data);
                break;
            case 'call-answer':
                await this.handleCallAnswer(data);
                break;
            case 'ice-candidate':
                await this.handleIceCandidate(data);
                break;
            case 'call-rejected':
                this.handleCallRejected();
                break;
            case 'call-ended':
                this.endCall();
                break;
            case 'call-timeout':
                this.handleCallTimeout();
                break;
        }
    }

    // Start a call (audio or video)
    async startCall(callType) {
        this.callType = callType;

        try {
            // Get user media
            const constraints = {
                audio: true,
                video: callType === 'video'
            };

            this.localStream = await navigator.mediaDevices.getUserMedia(constraints);

            // Show call modal
            this.showCallModal('outgoing');

            // Set local video
            if (callType === 'video') {
                document.getElementById('localVideo').srcObject = this.localStream;
            }

            // Create peer connection
            this.createPeerConnection();

            // Add local stream to peer connection
            this.localStream.getTracks().forEach(track => {
                this.peerConnection.addTrack(track, this.localStream);
            });

            // Create and send offer
            const offer = await this.peerConnection.createOffer();
            await this.peerConnection.setLocalDescription(offer);

            this.sendSignalingMessage({
                type: 'call-offer',
                offer: offer,
                callType: callType,
                from: this.currentUserId,
                to: this.otherUserId
            });

            // Set timeout for unanswered call (30 seconds)
            this.callTimeout = setTimeout(() => {
                if (!this.callAnswered) {
                    this.sendSignalingMessage({
                        type: 'call-timeout',
                        from: this.currentUserId,
                        to: this.otherUserId
                    });
                    this.handleCallTimeout();
                }
            }, 30000); // 30 seconds

        } catch (error) {
            console.error('Error starting call:', error);
            alert('Could not access camera/microphone. Please check permissions.');
            this.closeCallModal();
        }
    }

    // Handle incoming call offer
    async handleCallOffer(data) {
        // Convert to numbers for comparison (data comes as string from JSON)
        if (parseInt(data.to) !== this.currentUserId) {
            console.log('Call not for me. Expected:', this.currentUserId, 'Got:', data.to);
            return;
        }

        this.callType = data.callType;
        console.log('Incoming call from user:', data.from, 'Type:', data.callType);

        // Show incoming call modal
        this.showCallModal('incoming', data.callType);

        // Store offer for later (when user accepts)
        this.pendingOffer = data.offer;
    }

    // Accept incoming call
    async acceptCall() {
        try {
            const constraints = {
                audio: true,
                video: this.callType === 'video'
            };

            this.localStream = await navigator.mediaDevices.getUserMedia(constraints);

            if (this.callType === 'video') {
                document.getElementById('localVideo').srcObject = this.localStream;
            }

            this.createPeerConnection();

            this.localStream.getTracks().forEach(track => {
                this.peerConnection.addTrack(track, this.localStream);
            });

            await this.peerConnection.setRemoteDescription(new RTCSessionDescription(this.pendingOffer));

            const answer = await this.peerConnection.createAnswer();
            await this.peerConnection.setLocalDescription(answer);

            this.sendSignalingMessage({
                type: 'call-answer',
                answer: answer,
                from: this.currentUserId,
                to: this.otherUserId
            });

            this.showCallModal('active');
            this.startCallTimer();

        } catch (error) {
            console.error('Error accepting call:', error);
            alert('Could not access camera/microphone.');
            this.rejectCall();
        }
    }

    // Reject incoming call
    rejectCall() {
        this.sendSignalingMessage({
            type: 'call-rejected',
            from: this.currentUserId,
            to: this.otherUserId
        });
        this.closeCallModal();
    }

    // Handle call answer
    async handleCallAnswer(data) {
        // Convert to numbers for comparison
        if (parseInt(data.to) !== this.currentUserId) {
            console.log('Call answer not for me. Expected:', this.currentUserId, 'Got:', data.to);
            return;
        }

        // Clear timeout since call was answered
        if (this.callTimeout) {
            clearTimeout(this.callTimeout);
            this.callTimeout = null;
        }
        this.callAnswered = true;

        await this.peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer));
        this.showCallModal('active');
        this.startCallTimer();
    }

    // Handle ICE candidate
    async handleIceCandidate(data) {
        // Convert to numbers for comparison
        if (parseInt(data.to) !== this.currentUserId) return;

        try {
            await this.peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate));
        } catch (error) {
            console.error('Error adding ICE candidate:', error);
        }
    }

    // Handle call rejected
    handleCallRejected() {
        // Clear timeout
        if (this.callTimeout) {
            clearTimeout(this.callTimeout);
            this.callTimeout = null;
        }
        alert('Call was rejected');
        this.closeCallModal();
    }

    // Create peer connection
    createPeerConnection() {
        this.peerConnection = new RTCPeerConnection(this.iceServers);

        // Handle ICE candidates
        this.peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
                this.sendSignalingMessage({
                    type: 'ice-candidate',
                    candidate: event.candidate,
                    from: this.currentUserId,
                    to: this.otherUserId
                });
            }
        };

        // Handle remote stream
        this.peerConnection.ontrack = (event) => {
            if (!this.remoteStream) {
                this.remoteStream = new MediaStream();
                document.getElementById('remoteVideo').srcObject = this.remoteStream;
            }
            this.remoteStream.addTrack(event.track);
        };
    }

    // Send signaling message via WebSocket
    sendSignalingMessage(message) {
        if (this.callSocket && this.callSocket.readyState === WebSocket.OPEN) {
            this.callSocket.send(JSON.stringify(message));
        } else {
            console.error('WebSocket is not open. ReadyState:', this.callSocket ? this.callSocket.readyState : 'null');
            // Try to reconnect if socket is closed
            if (!this.callSocket || this.callSocket.readyState === WebSocket.CLOSED) {
                console.log('Attempting to reconnect WebSocket...');
                this.initializeWebSocket();
                // Retry sending message after a short delay
                setTimeout(() => {
                    if (this.callSocket && this.callSocket.readyState === WebSocket.OPEN) {
                        this.callSocket.send(JSON.stringify(message));
                    }
                }, 1000);
            }
        }
    }

    // End call
    endCall() {
        // Calculate call duration if call was active
        let duration = 0;
        if (this.callStartTime) {
            duration = Math.floor((Date.now() - this.callStartTime) / 1000);
        }

        this.sendSignalingMessage({
            type: 'call-ended',
            from: this.currentUserId,
            to: this.otherUserId,
            duration: duration
        });

        this.cleanup();
        this.closeCallModal();
    }

    // Handle call timeout (missed call)
    handleCallTimeout() {
        alert('Call not answered');
        this.closeCallModal();
    }

    // Cleanup resources
    cleanup() {
        if (this.callTimerInterval) {
            clearInterval(this.callTimerInterval);
        }

        if (this.callTimeout) {
            clearTimeout(this.callTimeout);
        }

        if (this.localStream) {
            this.localStream.getTracks().forEach(track => track.stop());
        }

        if (this.peerConnection) {
            this.peerConnection.close();
        }

        // DO NOT close the WebSocket - it needs to stay open for future calls
        // Only close it when the page is unloaded or user navigates away

        this.localStream = null;
        this.remoteStream = null;
        this.peerConnection = null;
        this.callTimeout = null;
        this.callAnswered = false;
        this.callStartTime = null;
        this.callTimerInterval = null;
    }

    // Toggle mute
    toggleMute() {
        if (this.localStream) {
            const audioTrack = this.localStream.getAudioTracks()[0];
            audioTrack.enabled = !audioTrack.enabled;
            const muteBtn = document.getElementById('muteBtn');
            muteBtn.classList.toggle('bg-red-600');
            muteBtn.classList.toggle('bg-slate-600');
        }
    }

    // Toggle video
    toggleVideo() {
        if (this.localStream && this.callType === 'video') {
            const videoTrack = this.localStream.getVideoTracks()[0];
            videoTrack.enabled = !videoTrack.enabled;
            const videoBtn = document.getElementById('videoBtn');
            videoBtn.classList.toggle('bg-red-600');
            videoBtn.classList.toggle('bg-slate-600');
        }
    }

    // Start call timer
    startCallTimer() {
        this.callStartTime = Date.now();
        this.callTimerInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - this.callStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            document.getElementById('callTimer').textContent =
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    }

    // Show call modal
    showCallModal(state, callType = this.callType) {
        const modal = document.getElementById('callModal');
        const incomingCall = document.getElementById('incomingCall');
        const outgoingCall = document.getElementById('outgoingCall');
        const activeCall = document.getElementById('activeCall');

        // Hide all states
        incomingCall.classList.add('hidden');
        outgoingCall.classList.add('hidden');
        activeCall.classList.add('hidden');

        // Show appropriate state
        if (state === 'incoming') {
            incomingCall.classList.remove('hidden');
            document.getElementById('incomingCallType').textContent =
                callType === 'video' ? 'Video Call' : 'Audio Call';
        } else if (state === 'outgoing') {
            outgoingCall.classList.remove('hidden');
            document.getElementById('outgoingCallType').textContent =
                callType === 'video' ? 'Video Call' : 'Audio Call';
        } else if (state === 'active') {
            activeCall.classList.remove('hidden');
            if (callType === 'video') {
                document.getElementById('videoContainer').classList.remove('hidden');
            } else {
                document.getElementById('videoContainer').classList.add('hidden');
            }
        }

        modal.classList.remove('hidden');
    }

    // Close call modal
    closeCallModal() {
        document.getElementById('callModal').classList.add('hidden');
        this.cleanup();
    }

    // Properly close WebSocket when page unloads
    destroy() {
        this.cleanup();
        if (this.callSocket) {
            this.callSocket.close();
            this.callSocket = null;
        }
    }
}

// Global call manager instance
let callManager = null;

// Clean up WebSocket when page unloads
window.addEventListener('beforeunload', () => {
    if (callManager) {
        callManager.destroy();
    }
});
