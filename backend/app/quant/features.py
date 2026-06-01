import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

class TransformerFeatureExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space, features_dim: int = 64, heads: int = 4, layers: int = 2):
        super().__init__(observation_space, features_dim)
        input_dim = observation_space.shape[0]
        self.embedding = nn.Linear(input_dim, features_dim)
        encoder_layer = nn.TransformerEncoderLayer(d_model=features_dim, nhead=heads, batch_first=True)
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=layers)
        self.output = nn.Linear(features_dim, features_dim)

    def forward(self, observations: torch.Tensor) -> torch.Tensor:
        x = self.embedding(observations).unsqueeze(1)
        x = self.encoder(x)
        return self.output(x.squeeze(1))
