def test(light1, light2, light3, light4):
        light1.duty_cycle=65535
        light2.duty_cycle=65535
        light3.duty_cycle=65535
        light4.duty_cycle=65535
        print("deftestcheck")

test(pca.channels[0], pca.channels[1], pca.channels[2], pca.channels[3])
