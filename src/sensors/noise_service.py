from enviroplus.noise import Noise

noise = Noise()


def get_noise_measurement():
    return noise.get_noise_profile()
