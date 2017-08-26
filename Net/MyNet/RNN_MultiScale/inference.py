# -*- coding: utf-8 -*-
from Config import Config
from Net.tools import do_conv, FC_layer, pool, convert_two_dim, batch_norm
import tensorflow as tf


# input_tensor [batch_size, w, h, 3]
def inference(input_tensors, regularizer):
    CONV_LAYER_OUT = None
    for index, input_tensor in enumerate(input_tensors):
        # 对于每个尺度的图像，进行下面的ＲＮＮ-Part
        input_shape = input_tensor.get_shape().as_list()
        state = tf.zeros(
            [
                Config.BATCH_SIZE,
                Config.STATE_FEATURE_DIM
            ]
        )
        with tf.variable_scope('rnn-part-'+str(index), reuse=False):
            # 对不同phase之间参数的一样的
            for i in range(input_shape[3]):
                if i == 0:
                    reuse = False
                else:
                    reuse = True
                cur_input = input_tensor[:, :, :, i]
                cur_input = tf.reshape(
                    cur_input,
                    [
                        input_shape[0],
                        input_shape[1],
                        input_shape[2],
                        1
                    ]
                )
                for key in Config.CONV_LAYERS_CONFIG:
                    layer_config = Config.CONV_LAYERS_CONFIG[key]
                    conv_res = do_conv(
                        key,
                        cur_input,
                        layer_config['deep'],
                        [layer_config['size'], layer_config['size']],
                        dropout=layer_config['dropout'],
                        reuse=reuse

                    )
                    cur_input = conv_res
                    if layer_config['pooling']['exists']:
                        pooling = pool(
                            layer_config['pooling']['name'],
                            cur_input
                        )
                        cur_input = pooling
                # 完成了卷积操作
                cur_input = convert_two_dim(cur_input)  # 展成二维的变量
                print cur_input
                cur_input = tf.concat([cur_input, state], axis=1)
                print cur_input
                state = FC_layer('extract_state', cur_input, Config.STATE_FEATURE_DIM, regularizer, reuse)  # 更新状态

            if CONV_LAYER_OUT is None:
                CONV_LAYER_OUT = state
            else:
                CONV_LAYER_OUT = tf.concat([CONV_LAYER_OUT, state], axis=1)

    input_tensor = CONV_LAYER_OUT
    for key in Config.FC_LAYERS_CONFIG:
        layer_config = Config.FC_LAYERS_CONFIG[key]
        if not layer_config['regularizer']:
            cur_regularizer = None
        else:
            cur_regularizer = regularizer
        input_tensor = FC_layer(
            key,
            input_tensor,
            layer_config['size'],
            cur_regularizer
        )
        if layer_config['batch_norm']:
            input_tensor = batch_norm(input_tensor)
    return input_tensor


if __name__ == '__main__':
    x1 = tf.placeholder(
        tf.float32,
        [
            35, 45, 45, 3
        ]
    )
    x2 = tf.placeholder(
        tf.float32,
        [
            35, 100, 100, 3
        ]
    )
    y = inference([x1, x2], None)
    print y