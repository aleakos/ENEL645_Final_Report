pooling = [None, "max", "average"]
flip_aug = [None, "horizontal_and_vertical"]
rotation_aug = [None, 0.1, 0.2]
translation_aug = [None, 0.1, 0.2]


def make_names():
    names = []
    for pool in pooling:
        pool_name = f"pooling_{str(pool)}"
        for flip in flip_aug:
            flip_name = pool_name + f"_flip_{flip}"
            for rotation in rotation_aug:
                rotation_name = flip_name + f"_rotation_{rotation}"
                for translation in translation_aug:
                    translation_name = rotation_name + f"_translation_{translation}"
                    names.append(translation_name)
                    print(translation_name)
                    translation_name = rotation_name
    return names


print(len(make_names()))
