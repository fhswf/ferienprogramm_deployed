# Ferienprogramm KI

Ferienprogramm KI der Fachhochschule Südwestfalen für 2023.

## Tag 1: Neuronales Netz für Ziffernerkennung
Siehe [MNIST Notebook](Bildklassifikation/MNIST.ipynb)

### Training der Bildklassifikation auf dem KI-Cluster der Fachhochschule Südwestfalen

1. Melde Dich sich unter [ki.fh-swf.de/jupyterhub](https://www.ki.fh-swf.de/jupyterhub) an. Die Zugangsdaten erhälst Du im Kurs.
2. Klicke **danach** auf diesen [Link](https://www.ki.fh-swf.de/jupyterhub/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2Ffhswf%2FFerienkursKI.git&urlpath=lab%2Ftree%2FFerienkursKI.git%2FBildklassifikation%2FMNIST.ipynb&branch=main)

CNN für MGI:

```Python
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3)
        self.fc1 = nn.Linear(64*5*5, 128)
        self.fc2 = nn.Linear(128, 10)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 64*5*5)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x
```

## Tag 2: KI für Snake
Siehe Ordner [SnakeAI](SnakeAI)

## Tag 3: ChatBot zu Pokemon
Siehe Ordner [Chatbot](Chatbot)





[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fhswf/FerienkursKI/blob/main/Bildklassifikation/MNIST.ipynb)
