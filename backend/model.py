from transformers import BertConfig, BertForSequenceClassification, BertTokenizerFast

# 1) Carrega o tokenizer e obtém o tamanho real do vocabulário
tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased")
vocab_size = tokenizer.vocab_size

# 2) Define a configuração já com o vocab_size correto
config = BertConfig(
    vocab_size=vocab_size,  # agora igual ao tokenizer
    hidden_size=256,
    num_hidden_layers=4,
    num_attention_heads=8,
    intermediate_size=512,
    max_position_embeddings=512,
    type_vocab_size=2,
    num_labels=3,
)

# 3) Instancia o modelo com essa configuração
model = BertForSequenceClassification(config)
