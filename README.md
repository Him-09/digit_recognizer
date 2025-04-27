# Digit Recognizer

Digit Recognizer is a deep learning project for recognizing two-digit numbers (00-99) and detecting the absence of a number (no-number) from images. The project is implemented in Python using PyTorch and includes a Flutter app for desktop integration.

## Features
- Deep learning model for two-digit number recognition (00-99)
- Special handling for 'no-number' class
- Class balancing using computed class weights
- Cosine annealing learning rate scheduler with warmup
- Training and validation history logging
- Model checkpointing for best validation accuracy
- Flutter desktop app integration (Windows)

## Project Structure
```
best_model3.pth                # Best model weights
explanation_book.md            # Project explanations
LICENSE                        # License file
project_report.md              # Project report
README.md                      # This file
requirements.txt               # Python dependencies
training_history3.csv          # Training/validation history
flutter_app/                   # Flutter desktop app
ocr/                           # OCR-related code/data
src/                           # Main Python source code
    data/                      # Data loading utilities
    models/                    # Model definition
    ...                        # Training, evaluation, API, etc.
tirextract/                    # Additional code/widgets
```

## Getting Started

### Prerequisites
- Python 3.8+
- PyTorch
- (Optional) CUDA-enabled GPU for faster training
- Flutter (for desktop app)

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Him-09/digit_recognizer.git
   cd digit_recognizer
   ```
2. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. (Optional) Set up the Flutter app:
   - Follow instructions in `flutter_app/README.md` (if available)

### Training the Model
Run the following command to start training:
```sh
python src/train.py
```
- Training and validation metrics will be saved to `training_history3.csv`.
- The best model weights will be saved to `best_model3.pth`.

### Evaluating the Model
Use `src/evaluate.py` to evaluate the trained model on test data.

### API Usage
- The `src/api.py` file provides an API for model inference.

## Data
- Training/validation images: `src/train&valdata/`
- Labels: `src/data_label.csv`
- Test images: `src/testdata/`

## Model
- Model architecture is defined in `src/models/model.py` as `MyModel`.
- Handles 100 classes (00-99) plus a special 'no-number' class (index 100).

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- PyTorch
- Flutter
- Contributors and open-source community
