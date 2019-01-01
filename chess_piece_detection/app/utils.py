# system imports
import os
import itertools
import matplotlib.pyplot as plt

# Keras/TF imports
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input

# custom imports
import constants
import appconfigs


def get_required_data_with_labels_for_model(base_location, num_samples=None, dimensions=(299, 299)):
    X, y = [], []
    for class_name in constants.class_names_folder_mappings:
        for folder_name in constants.class_names_folder_mappings[class_name]:
            complete_path = os.path.join(base_location, folder_name)
            print("Reading the files from the location {0}".format(
                complete_path))
            current_samples = 0
            for image_file_name in os.listdir(complete_path):

                # check if the current file is an image file with jpg extension
                if image_file_name.endswith(".jpg"):
                    current_samples += 1
                    img_path = os.path.join(complete_path, image_file_name)

                    # basic pre-processing of the images
                    img = image.load_img(img_path, target_size=dimensions)
                    x = image.img_to_array(img)
                    x = preprocess_input(x)

                    X.append(x)
                    class_name_id = constants.class_names_reverse_mappings[class_name]
                    y.append(class_name_id)

                    if ((num_samples is not None) and (current_samples == num_samples)):
                        break

    return X, y


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()


def plot_train_validation_accuracy(historyobj):
    plt.plot(historyobj.history['acc'])
    plt.plot(historyobj.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

def create_artifact_folders():
    if not os.path.exists(appconfigs.model_folder_location):
        os.makedirs(appconfigs.model_folder_location)

    if not os.path.exists(appconfigs.tensorboard_logs_folder_location):
        os.makedirs(appconfigs.tensorboard_logs_folder_location)  