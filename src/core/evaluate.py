import string
import torch
from core.model import RNN

all_characters = string.printable
n_characters = len(all_characters)

device = "cuda:0" if torch.cuda.is_available() else "cpu"


def char_tensor(string):
    tensor = torch.zeros(len(string)).long()
    for c in range(len(string)):
        tensor[c] = all_characters.index(string[c])
    return tensor


def generate(model, initial_str="amazing", predict_len=100, temperature=0.85):
    hidden, cell = model.init_hidden(batch_size=1)
    initial_input = char_tensor(initial_str)
    predicted = initial_str

    for p in range(len(initial_str) - 1):
        _, (hidden, cell) = model(
            initial_input[p].view(1).to(device), hidden, cell
        )

    last_char = initial_input[-1]

    for p in range(predict_len):
        output, (hidden, cell) = model(
            last_char.view(1).to(device), hidden, cell
        )
        output_dist = output.data.view(-1).to(device).div(temperature).exp()
        top_char = torch.multinomial(output_dist, 1)[0]
        predicted_char = all_characters[top_char]
        predicted += predicted_char
        last_char = char_tensor(predicted_char)

    return predicted