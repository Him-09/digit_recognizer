import torch
import pandas as pd


def save_predictions(model, test_dataloader, device, filename='predictions.csv'):
    predictions = []
    true_labels = []

    model.eval()
    with torch.no_grad():
        for images, labels in test_dataloader:
            images = images.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            predictions.extend(predicted.cpu().numpy())
            true_labels.extend(labels.numpy())

    df = pd.DataFrame({
        'image_name': test_dataloader.dataset.data.iloc[:, 0],
        'true_label': true_labels,
        'predicted_label': predictions
    })

    df['true_label'] = df['true_label'].apply(lambda x: 'nan' if x == -1 else x)
    df['predicted_label'] = df['predicted_label'].apply(lambda x: 'nan' if x == 0 else x - 1)

    df.to_csv(filename, index=False)


def train(model, train_dataloader, val_dataloader, optimizer, scheduler, criterion, num_epochs, device):
    best_val_loss = float('inf')
    history = []

    for epoch in range(num_epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        no_number_correct = 0
        no_number_total = 0

        for images, labels in train_dataloader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels + 1)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels + 1).sum().item()

            no_number_mask = (labels == -1)
            if no_number_mask.any():
                no_number_total += no_number_mask.sum().item()
                no_number_correct += (predicted[no_number_mask] == 0).sum().item()

        train_loss = running_loss / len(train_dataloader)
        train_accuracy = 100. * correct / total
        no_number_accuracy = 100. * no_number_correct / no_number_total if no_number_total > 0 else 0

        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        val_no_number_correct = 0
        val_no_number_total = 0

        with torch.no_grad():
            for images, labels in val_dataloader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels + 1)

                val_loss += loss.item()
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels + 1).sum().item()

                no_number_mask = (labels == -1)
                if no_number_mask.any():
                    val_no_number_total += no_number_mask.sum().item()
                    val_no_number_correct += (predicted[no_number_mask] == 0).sum().item()

        val_loss = val_loss / len(val_dataloader)
        val_accuracy = 100. * val_correct / val_total
        val_no_number_accuracy = 100. * val_no_number_correct / val_no_number_total if val_no_number_total > 0 else 0

        scheduler.step(val_loss)
        current_lr = optimizer.param_groups[0]['lr']

        print(f'Epoch {epoch + 1}/{num_epochs}:')
        print(f'Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.2f}%')
        print(f'Train No-Number Accuracy: {no_number_accuracy:.2f}%')
        print(f'Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.2f}%')
        print(f'Val No-Number Accuracy: {val_no_number_accuracy:.2f}%')
        print(f'Learning Rate: {current_lr:.6f}\n')

        history.append({
            'epoch': epoch + 1,
            'train_loss': train_loss,
            'train_accuracy': train_accuracy,
            'no_number_accuracy': no_number_accuracy,
            'val_loss': val_loss,
            'val_accuracy': val_accuracy,
            'val_no_number_accuracy': val_no_number_accuracy,
            'learning_rate': current_lr
        })

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': best_val_loss,
                'train_loss': train_loss,
            }, 'best_model1.pth')

    pd.DataFrame(history).to_csv('training_history1.csv', index=False)
    return history


def evaluate(model, test_dataloader, num_classes, device):
    model.eval()
    correct = 0
    total = 0
    no_number_correct = 0
    no_number_total = 0

    with torch.no_grad():
        for images, labels in test_dataloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels + 1).sum().item()

            no_number_mask = (labels == -1)
            if no_number_mask.any():
                no_number_total += no_number_mask.sum().item()
                no_number_correct += (predicted[no_number_mask] == 0).sum().item()

    accuracy = 100. * correct / total
    no_number_accuracy = 100. * no_number_correct / no_number_total if no_number_total > 0 else 0

    print('\nTest Results:')
    print(f'Overall Accuracy: {accuracy:.2f}%')
    print(f'No-Number Detection Accuracy: {no_number_accuracy:.2f}%')

    return accuracy