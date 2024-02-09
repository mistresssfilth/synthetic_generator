import numpy as np
import pandas as pd
from keras.initializers.initializers_v1 import RandomNormal
from keras.layers import Input, Dense, Dropout, LeakyReLU
from keras.models import Model, Sequential
from keras.optimizers import RMSprop
from keras.utils import Progbar
import keras.backend as K


class Gan:
    def __init__(self, real_scaled_data, col_max_array):
        self.real_data = real_scaled_data
        self.col_max_array = pd.DataFrame(col_max_array).T
        self.data_dim = len(real_scaled_data.columns)
        self.latent_dim = 100
        self.base_n_count = 256
        self.d_iters = 5

        optimizer = RMSprop(lr=0.00005)

        self.discriminator = self.build_discriminator()
        self.discriminator.compile(
            loss=self.wasserstein_loss,
            optimizer=optimizer,
        )

        self.generator = self.build_generator()

        z = Input(shape=(self.latent_dim,), name='input_z')
        generated_data = self.generator(z)

        is_fake = self.discriminator(generated_data)

        self.combined = Model(z, is_fake)
        self.combined.get_layer('D').trainable = False
        self.combined.compile(loss=self.wasserstein_loss, optimizer=optimizer)

    def build_generator(self):

        weight_init = RandomNormal(mean=0., stddev=0.02)
        model = Sequential()

        model.add(Dense(self.base_n_count, input_dim=self.latent_dim))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(self.base_n_count * 2))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(self.base_n_count * 4))
        model.add(LeakyReLU(alpha=0.2))

        model.add(Dense(self.data_dim, activation='tanh'))

        noise = Input(shape=(self.latent_dim,))
        fake_data = model(noise)

        print(model.summary())

        return Model(noise, fake_data, name='G')

    def build_discriminator(self):

        weight_init = RandomNormal(mean=0., stddev=0.02)
        model = Sequential()

        model.add(Dense(self.base_n_count * 4, input_dim=self.data_dim))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.3))
        model.add(Dense(self.base_n_count * 2))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.3))
        model.add(Dense(self.base_n_count))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.3))
        model.add(Dense(1, activation='linear'))

        print(model.summary())

        data_features = Input(shape=(self.data_dim,))
        is_fake = model(data_features)

        return Model(data_features, is_fake, name='D')

    def train(self, epochs, batch_size, sample_size):
        self.fake_data_list = []
        self.epoch_gen_loss = []
        self.epoch_disc_true_loss = []
        self.epoch_disc_fake_loss = []
        nb = int(sample_size / batch_size) * epochs
        rounds = int(sample_size / batch_size)

        progress_bar = Progbar(target=nb)

        for index in range(nb):
            x_train = self.real_data.sample(sample_size)
            progress_bar.update(index)
            for d_it in range(self.d_iters):
                # unfreeze D
                self.discriminator.trainable = True
                for l in self.discriminator.layers:
                    l.trainable = True

                # clip D weights
                for l in self.discriminator.layers:
                    weights = l.get_weights()
                    weights = [np.clip(w, -0.01, 0.01) for w in weights]
                    l.set_weights(weights)

                # Maximize D output on reals == minimize -1*(D(real)) and get a batch of real data
                data_index = np.random.choice(len(x_train), batch_size, replace=False)
                data_batch = x_train.values[data_index]

                self.epoch_disc_true_loss.append(self.discriminator.train_on_batch(data_batch, -np.ones(batch_size)))

                # Minimize D output on fakes
                # generate a new batch of noise
                noise = np.random.normal(loc=0.0, scale=1, size=(int(batch_size), self.latent_dim))

                generated_data = self.generator.predict(noise, verbose=0)
                self.epoch_disc_fake_loss.append(
                    self.discriminator.train_on_batch(generated_data, np.ones(int(batch_size))))

            # freeze D and C
            self.discriminator.trainable = False
            for l in self.discriminator.layers:
                l.trainable = False

            noise = np.random.normal(loc=0.0, scale=1, size=(int(batch_size), self.latent_dim))
            self.epoch_gen_loss.append(self.combined.train_on_batch(noise, -np.ones(int(batch_size))))

    def wasserstein_loss(y_true, y_pred):
        # Returns the result of the wasserstein loss function.
        return K.mean(y_true * y_pred)

    def gen_fake_data(self, epochs=100):
        # Uses generator to generate fake data.
        fake_data = pd.DataFrame()

        for x in range(epochs):
            noise = np.random.normal(0, 1, (1, self.latent_dim))
            gen_data = self.generator.predict(noise)
            gen_data = gen_data * self.col_max_array
            fake_data = fake_data._append(gen_data)

        return fake_data
