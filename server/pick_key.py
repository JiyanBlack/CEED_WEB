from random import shuffle


def pick_key():
    key_pool = [
        "AIzaSyDMwaHBaOiPQlKZgyKhuuuBz2LTXgkZs5o",
        "AIzaSyDg8lUiahxeP68SEeQklI4sTAQXOdmyEUQ",
        "AIzaSyCQqUTOyGb_Lzk_2jgfUTNswITr7USyenM",
        "AIzaSyAGgz_a8FVJySZigTNVXemc22rEfKITABs",
        "AIzaSyCT7p5M-QiFLdNVSQZ7g3imhUIVBvd1LGI",
        "AIzaSyDrFbVJx4QHEUy_LrG3H0sbaCqtzNYDWFc",
        "AIzaSyDPxAR82-3huRVwzs1Z8qHHXgvicyASS98",
        "AIzaSyAeSZDflSgsECfwg8CfCnwzkmgDUeScUlk",
        "AIzaSyCj-JvaXt6m7ko-Nq9BzlVT1dfmYAM5pE8",
        "AIzaSyArpqHUmePG2km3eMuCEUAFrEWDJTnnewM",
        "AIzaSyDY4mp03QM9_e-ouCkeBziZzHzr0K6zCbM",
        "AIzaSyAqpOEgC3t9p6fQbG48djvsGA3KCbyVNtc",
        "AIzaSyCkx_e6Xtmx691UklXLj3gpRd-KhTvZMAw",
        "AIzaSyA3QdMS3b2MdsNQFYnc3O6AGIV1LSRKEH4",
        "AIzaSyDMj9k4ReFMeyzlg_HEa02NdMX1dWN3f3A",
        "AIzaSyAa7wPbLFugvf9UtMQnnAhsraQJjZpbN58",
        "AIzaSyD1iNYWuCgUwfYh9f7YyyF7od-yUZ-p-0k",
        "AIzaSyCwEUq8-3s_BK66XMHzxaTHD5ye-nProMU",
        "AIzaSyC7FCbIc7fh5wY4SvxjQlEUCGzP7h1hr3Y",
        "AIzaSyBei_kxrqeVV200i66b7ebWa8N0RMvYzhs",
        "AIzaSyCsBmdATgysDB4g2-dqukRDWQH2vntg6lo",
        "AIzaSyDfs4swr30oBO0vbnYhFXK8d9lHX0s3c1w",
        "AIzaSyBUSdWi_Yyi1KPgJsSzGjWLELqDSYQ5t0E",
        "AIzaSyBw5zV0rNQQwR8179pgGXdkWy181RBryCc",
        "AIzaSyBIMiTr0StX9Rie4e81ckitPjQquXHdYwk",
        "AIzaSyDVHCkTrS4flwaiy1FYdz-LnRF2B3qIXGE",
        "AIzaSyCQH5wJMq2T8iePN-6QycT2fF1S29YGPn8",
        "AIzaSyDsz9QoVqVW_8JQx7DvOyU71ir2lo750Gk",
        "AIzaSyDGYjS-zWnct0ueYhXW5iFzxSRnSNeYmUg",
        "AIzaSyCG8OzN1DVznjxFJ8QM8-Ygzs8wO5yKyf8",
        "AIzaSyBtQBWRvLaOtLoYMLg3R-IeiU-27pUFKKU",
    ]
    shuffle(key_pool)
    key_number = len(key_pool)
    cur = 0
    while True:
        yield key_pool[cur]
        cur = (cur + 1) % key_number
