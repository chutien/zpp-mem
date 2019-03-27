default_network = {
    # constructor parameters
    "type": "BP",
    "dataset_name": "mnist",
    "sequence": "blocks_50_30_10_bn_sigmoid",
    "cost_function": "mean_squared_error",
    "learning_rate": 0.1,
    "gather_stats": True,
    "restore_model": False,
    "save_model": False,
    "restore_model_path": None,
    "save_model_path": None,

    # train parameters
    "batch_size": 10,
    "epochs": 4,
    "eval_period": 1000,
    "stat_period": 100,
    "memory_only": False,
    "seed": None,
    "device": "/cpu:0"
}

memory_testing_network = dict(default_network)
memory_testing_network.update({
    "sequence": "blocks_30x500_10_bn_sigmoid",
    "memory_only": True
})

simple_convolutional_network = dict(default_network)
simple_convolutional_network.update({
    "sequence": "blocks_simple_convoluted",
})
simple_convolutional_network_pool = dict(default_network)
simple_convolutional_network_pool.update({
    "sequence": "blocks_simple_convoluted_with_pool",
})

simple_convolutional_manhattan_network = dict(default_network)
simple_convolutional_manhattan_network.update({
    "sequence": "blocks_simple_convoluted_bm",
})

simple_fully_connected_manhattan_network = dict(default_network)
simple_fully_connected_manhattan_network.update({
    "sequence": "blocks_50_30_10_bn_bm_sigmoid",
})

resnetish = dict(default_network)
resnetish.update({
    "dataset_name": "cifar10",

    #"sequence": "blocks_3x50_10_residual_relu",
     "sequence": "mini_resnet",

})


