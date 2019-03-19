default_network = {
    # constructor parameters
    "type": "BP",
    "dataset_name": "mnist",
    "sequence": "blocks_50_30_10_bn_sigmoid",
    "learning_rate": 0.1,
    "gather_stats": False,
    "restore_model": False,
    "save_model": False,
    # "restore_model_path": "./saved_model/model.ckpt",
    # "save_model_path": "./saved_model/model.ckpt",

    # train parameters
    "batch_size": 20,
    "epochs": 2,
    "eval_period": 1000,
    "stat_period": 100,
    "memory_only": False
}

memory_testing_network = dict(default_network)
memory_testing_network.update({
    "sequence": "blocks_30x500_10_bn_sigmoid",
    "memory_only": True
})
