# keras_yolo_v2

# YOLOv2 in Keras and Applications

This repo contains the implementation of YOLOv2 in Keras with Tensorflow backend for identifying the icons in Apple Carplay homescreen.

## Some example applications (click for videos):

### Carplay Homescreen Icons detection

Run generate_index.py in ./carplay with the image carplay.png:
python generate_index.py --image carplay.png
It will export images in ./carplay/images and annotations in ./carplay/annotations

## Usage for python code

### 0. Requirement

python 3.5

keras >= 2.0.8

imgaug

tensorflow 1.15

### 1. Data preparation
In config.json, change the train folder to ./carplay/images

+ train_image_folder <= the folder that contains the train images.

In config.json, change the annotation folder to ./carplay/annotations

+ train_annot_folder <= the folder that contains the train annotations in VOC format.

There is a one-to-one correspondence by file name between images and annotations. If the validation set is empty, the training set will be automatically splitted into the training set and validation set using the ratio of 0.8.

### 2. Edit the configuration file
The configuration file is a json file, which looks like this:

```python
{
    "model" : {
        "architecture":         "Full Yolo",    # "Tiny Yolo" or "Full Yolo" or "MobileNet" or "SqueezeNet" or "Inception3"
        "input_size":           416,
        "anchors":              [1.88,3.13, 1.88,3.13, 1.88,3.13, 1.88,3.13, 1.88,3.13],
        "max_box_per_image":    10,        
        "labels":               ["phone", "music", "maps", "messages", "playing", "podcasts", "audiobook", "audiotest"]
    },

    "train": {
        "train_image_folder":   "/home/xueguang/coding/machine_learning/keras-yolo2-master/carplay/images_tiny/",
        "train_annot_folder":   "/home/xueguang/coding/machine_learning/keras-yolo2-master/carplay/annotations_tiny/",      
          
        "train_times":          10,             # the number of time to cycle through the training set, useful for small datasets
        "pretrained_weights":   "",             # specify the path of the pretrained weights, but it's fine to start from scratch
        "batch_size":           2,             # the number of images to read in each batch
        "learning_rate":        1e-5,           # the base learning rate of the default Adam rate scheduler
        "nb_epoch":             10,             # number of epoches
        "warmup_epochs":        3,              # the number of initial epochs during which the sizes of the 5 boxes in each cell is forced to match the sizes of the 5 anchors, this trick seems to improve precision emperically

        "object_scale":         5.0 ,           # determine how much to penalize wrong prediction of confidence of object predictors
        "no_object_scale":      1.0,            # determine how much to penalize wrong prediction of confidence of non-object predictors
        "coord_scale":          1.0,            # determine how much to penalize wrong position and size predictions (x, y, w, h)
        "class_scale":          1.0,            # determine how much to penalize wrong class prediction

        "debug":                true            # turn on/off the line that prints current confidence, position, size, class losses and recall
    },

    "valid": {
        "valid_image_folder":   "",
        "valid_annot_folder":   "",

        "valid_times":          1
    }
}

```

The model section defines the type of the model to construct as well as other parameters of the model such as the input image size and the list of anchors. The ```labels``` setting lists the labels to be trained on. Only images, which has labels being listed, are fed to the network. The rest images are simply ignored. By this way, a Dog Detector can easily be trained using VOC or COCO dataset by setting ```labels``` to ```['dog']```.

### 3. Generate anchors for your dataset (optional)

`python gen_anchors.py -c config.json`

Copy the generated anchors printed on the terminal to the ```anchors``` setting in ```config.json```.

### 4. Start the training process

`python train.py -c config.json`

By the end of this process, the code will write the weights of the best model to file best_weights.h5 (or whatever name specified in the setting "saved_weights_name" in the config.json file). The training process stops when the loss on the validation set is not improved in 3 consecutive epoches.

### 5. Perform detection using trained weights on an image by running
`python predict.py -c config.json -i /path/to/image/or/video`

It carries out detection on the image and write the image with detected bounding boxes to the same folder.

### 6. Check the process using tensorboard
`tensorboard --logdir ./logs/20200207181450`

It carries out detection on the image and write the image with detected bounding boxes to the same folder.

## Copyright

See [LICENSE](LICENSE) for details.
