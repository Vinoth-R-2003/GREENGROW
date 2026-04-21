"""
Training script for the Plant Disease Detection CNN model.

Based on the architecture from Train_Plant_disease.ipynb.
Trains on the PlantVillage dataset (38 classes).

Usage:
    python checks/train_model.py --train_dir <path_to_train_folder> --valid_dir <path_to_valid_folder>

The trained model is saved to checks/ml_models/trained_plant_disease_model.keras
"""

import os
import sys
import argparse


def build_model():
    """Build the CNN model matching the notebook architecture."""
    import tensorflow as tf

    cnn = tf.keras.models.Sequential()

    # Block 1: 32 filters
    cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding='same',
                                    activation='relu', input_shape=[128, 128, 3]))
    cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

    # Block 2: 64 filters
    cnn.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding='same',
                                    activation='relu'))
    cnn.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

    # Block 3: 128 filters
    cnn.add(tf.keras.layers.Conv2D(filters=128, kernel_size=3, padding='same',
                                    activation='relu'))
    cnn.add(tf.keras.layers.Conv2D(filters=128, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

    # Block 4: 256 filters
    cnn.add(tf.keras.layers.Conv2D(filters=256, kernel_size=3, padding='same',
                                    activation='relu'))
    cnn.add(tf.keras.layers.Conv2D(filters=256, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

    # Block 5: 512 filters
    cnn.add(tf.keras.layers.Conv2D(filters=512, kernel_size=3, padding='same',
                                    activation='relu'))
    cnn.add(tf.keras.layers.Conv2D(filters=512, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

    # Dropout + Flatten
    cnn.add(tf.keras.layers.Dropout(0.25))
    cnn.add(tf.keras.layers.Flatten())

    # Dense layers
    cnn.add(tf.keras.layers.Dense(units=1508, activation='relu'))
    cnn.add(tf.keras.layers.Dropout(0.4))

    # Output: 38 classes
    cnn.add(tf.keras.layers.Dense(units=38, activation='softmax'))

    # Compile
    cnn.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return cnn


def train(train_dir, valid_dir, epochs=10, output_path=None):
    """Train the model and save it."""
    import tensorflow as tf

    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, 'ml_models',
                                    'trained_plant_disease_model.keras')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"[INFO] Loading training data from: {train_dir}")
    training_set = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        labels="inferred",
        label_mode="categorical",
        color_mode="rgb",
        batch_size=32,
        image_size=(128, 128),
        shuffle=True,
    )

    print(f"[INFO] Loading validation data from: {valid_dir}")
    validation_set = tf.keras.utils.image_dataset_from_directory(
        valid_dir,
        labels="inferred",
        label_mode="categorical",
        color_mode="rgb",
        batch_size=32,
        image_size=(128, 128),
        shuffle=True,
    )

    # Print class names for verification
    print(f"[INFO] Classes found: {training_set.class_names}")
    print(f"[INFO] Number of classes: {len(training_set.class_names)}")

    # Build and train
    print("[INFO] Building model...")
    model = build_model()
    model.summary()

    print(f"[INFO] Training for {epochs} epochs...")
    history = model.fit(
        x=training_set,
        validation_data=validation_set,
        epochs=epochs,
    )

    # Evaluate
    print("[INFO] Evaluating on training set...")
    train_loss, train_acc = model.evaluate(training_set)
    print(f"  Training Loss: {train_loss:.4f}")
    print(f"  Training Accuracy: {train_acc:.4f}")

    print("[INFO] Evaluating on validation set...")
    val_loss, val_acc = model.evaluate(validation_set)
    print(f"  Validation Loss: {val_loss:.4f}")
    print(f"  Validation Accuracy: {val_acc:.4f}")

    # Save
    print(f"[INFO] Saving model to: {output_path}")
    model.save(output_path)
    print("[INFO] Training complete!")

    return history


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Train the Plant Disease Detection CNN model'
    )
    parser.add_argument('--train_dir', type=str, required=True,
                        help='Path to the training data directory')
    parser.add_argument('--valid_dir', type=str, required=True,
                        help='Path to the validation data directory')
    parser.add_argument('--epochs', type=int, default=10,
                        help='Number of training epochs (default: 10)')
    parser.add_argument('--output', type=str, default=None,
                        help='Output path for the trained model')

    args = parser.parse_args()
    train(args.train_dir, args.valid_dir, args.epochs, args.output)
