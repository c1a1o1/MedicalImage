class Config:
    NEED_MUL = True
    MODEL_LOAD_PATH = '/home/give/PycharmProjects/StomachCanner/classification/Net/VGG16/models_original/'
    MODEL_SAVE_PATH = '/home/give/PycharmProjects/StomachCanner/classification/Net/VGG16/models_original/'
    OUTPUT_NODE = 5
    TRAIN_BATCH_SIZE = 30
    TRAIN_BATCH_DISTRIBUTION = [
        15,    # cancer number
        15,    # non-cancer number
    ]

    IMAGE_W = 256
    IMAGE_H = 256
    IMAGE_CHANNEL = 1

    REGULARIZTION_RATE = 1e-3
    MOVEING_AVERAGE_DECAY = 0.9997

    LEARNING_RATE = 1e-3

    DROP_OUT = True

    ITERATOE_NUMBER = int(1e+4)

    TRAIN_LOG_DIR = '/home/give/PycharmProjects/StomachCanner/classification/Net/logs/train'
    VAL_LOG_DIR = '/home/give/PycharmProjects/StomachCanner/classification/Net/logs/val'
