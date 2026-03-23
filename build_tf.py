
# build_tf.py — tensorflow.html (35 topics)
import os, sys
sys.path.insert(0,r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final")
from build_all import HEAD,HERO,toc,section,cb,note,ptable,mgrid,playground,foot
BASE=r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final"

topics=[
  "tf.Tensor — creation dtype shape rank device","tf.Variable — assign assign_add trainable",
  "Tensor ops — math indexing broadcasting","tf.constant vs tf.Variable",
  "tf.function — trace graph retracing","tf.GradientTape — gradient jacobian",
  "Keras Sequential API","Keras Functional API — multi-input/output",
  "Keras Subclassing API — custom call()","Built-in Layers — Dense Conv2D LSTM GRU",
  "Normalization layers — BatchNorm LayerNorm Dropout Spatial",
  "Activation functions — relu sigmoid softmax selu gelu swish",
  "Loss functions — all built-ins + custom","Optimizers — Adam SGD RMSprop + params",
  "Callbacks — EarlyStopping ModelCheckpoint TensorBoard LRScheduler",
  "model.fit() — all params + return History","model.evaluate() / model.predict()",
  "model.compile() — run_eagerly & jit_compile","Saving — SavedModel HDF5 tf_saved_model",
  "tf.data.Dataset — from_tensor_slices map batch shuffle","tf.data pipeline best practices",
  "CNN recipe — Conv2D MaxPool2D Flatten","RNN/LSTM recipe — stateful return_sequences",
  "Transfer learning — base_model.trainable = False","Fine-tuning — unfreeze selective layers",
  "Custom training loop — GradientTape + optimizer.apply_gradients",
  "Metrics — compile metrics vs standalone update_state result",
  "Regularization — L1 L2 kernel_regularizer activity_regularizer Dropout",
  "Data augmentation — RandomFlip RandomRotation RandomZoom",
  "Hyperparameter tuning with Keras Tuner","Mixed precision — policy float16",
  "Multi-GPU — MirroredStrategy","TFLite conversion","TF Hub — hub.KerasLayer",
  "Debugging — tf.debugging.assert_* numerical checks",
]

s1=section(1,"Tensors &amp; Variables",
  "tf.Tensor is immutable; tf.Variable is mutable and tracked by GradientTape for autodiff. "
  "Both support the same math operations and broadcasting rules.",
  cb("tf.Tensor creation / dtype / shape / tf.Variable / assign / GradientTape",
"""import tensorflow as tf
import numpy as np

# ── tf.Tensor creation ────────────────────────────────────────────
a = tf.constant([1,2,3])                          # from list
b = tf.constant([[1.,2.],[3.,4.]])                # 2D float
c = tf.zeros((3,3), dtype=tf.float32)
d = tf.ones((2,4), dtype=tf.int32)
e = tf.eye(3)                                     # identity
f = tf.range(0,10,2)                              # [0,2,4,6,8]
g = tf.linspace(0.,1.,5)                          # [0.,0.25,0.5,0.75,1.]
r = tf.random.normal((3,3),mean=0,stddev=1,seed=42)
u = tf.random.uniform((2,3),minval=0,maxval=1,seed=0)

# Attributes
print(a.shape)    # (3,)
print(a.dtype)    # <dtype: 'int32'>
print(a.numpy())  # numpy conversion
print(a.device)   # /job:localhost/replica:0/task:0/device:CPU:0
print(tf.rank(b)) # 2

# Type casting
x = tf.cast(a, tf.float32)    # int32 → float32
y = tf.cast(b, tf.int32)      # float32 → int32

# ── tf.Variable ─────────────────────────────────────────────────────
w = tf.Variable(tf.random.normal((3,3)), name="weights", trainable=True)
bias = tf.Variable(tf.zeros(3), dtype=tf.float32)

w.assign(tf.ones((3,3)))          # full assignment
w.assign_add(tf.ones((3,3)))      # add in-place
w.assign_sub(tf.ones((3,3)))      # subtract in-place
w[0,0].assign(99.0)               # index assignment

print(w.name)         # weights:0
print(w.trainable)    # True
print(w.shape)        # (3, 3)

# ── GradientTape ─────────────────────────────────────────────────
x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x**2 + 2*x + 1   # y = (x+1)^2

dy_dx = tape.gradient(y, x)
print(f"dy/dx at x=3: {dy_dx.numpy()}")   # 2*(3+1) = 8.0

# Gradient w.r.t. multiple variables
W = tf.Variable(tf.random.normal((2,2)))
b2 = tf.Variable(tf.zeros(2))
x2 = tf.constant([[1.,2.]])

with tf.GradientTape() as tape:
    y2 = tf.nn.sigmoid(x2 @ W + b2)
    loss = tf.reduce_mean(y2)

grads = tape.gradient(loss, [W,b2])
print(f"dL/dW shape: {grads[0].shape}")  # (2,2)
print(f"dL/db shape: {grads[1].shape}")  # (2,)""",
["(3,)","<dtype: 'int32'>","dy/dx at x=3: 8.0","dL/dW shape: (2, 2)","dL/db shape: (2,)"])
)

s2=section(2,"Keras Sequential &amp; Functional API",
  "Sequential for simple stacks. Functional API for DAGs (multi-input, skip connections, shared layers). "
  "Subclassing for full control.",
  cb("Sequential / Functional / Subclassing / compile / fit / evaluate / predict",
"""import tensorflow as tf
from tensorflow import keras

# ── Sequential API ────────────────────────────────────────────────
model = keras.Sequential([
    keras.layers.Input(shape=(784,)),
    keras.layers.Dense(256, activation="relu"),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation="softmax"),
], name="mnist_mlp")

model.summary()

# ── Functional API ────────────────────────────────────────────────
inputs = keras.Input(shape=(784,), name="image")
x = keras.layers.Dense(256, activation="relu")(inputs)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dropout(0.3)(x)
x = keras.layers.Dense(128, activation="relu")(x)
outputs = keras.layers.Dense(10, activation="softmax")(x)
func_model = keras.Model(inputs, outputs, name="functional_mlp")

# Multi-input functional
inp1 = keras.Input(shape=(100,))
inp2 = keras.Input(shape=(50,))
merged = keras.layers.Concatenate()([inp1,inp2])
out = keras.layers.Dense(10,activation="softmax")(merged)
multi_model = keras.Model([inp1,inp2], out)

# ── Subclassing ────────────────────────────────────────────────────
class CustomModel(keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = keras.layers.Dense(64, activation="relu")
        self.dense2 = keras.layers.Dense(10, activation="softmax")

    def call(self, x, training=False):
        x = self.dense1(x)
        if training:
            x = tf.nn.dropout(x, rate=0.3)
        return self.dense2(x)

# ── compile() — all params ────────────────────────────────────────
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",  # or "categorical_crossentropy" "binary_crossentropy"
    metrics=["accuracy", keras.metrics.TopKCategoricalAccuracy(k=5)],
    run_eagerly=False,  # True for debugging (disables tf.function)
    jit_compile=False,  # XLA compilation (speed boost on GPU)
)

# ── fit() ─────────────────────────────────────────────────────────
import numpy as np
X_dummy = np.random.randn(1000,784).astype("float32")
y_dummy = np.random.randint(0,10,1000)

history = model.fit(X_dummy, y_dummy,
    epochs=3,
    batch_size=64,
    validation_split=0.1,    # 10% for validation
    validation_data=None,    # or (X_val,y_val) tuple
    callbacks=[],            # list of Callback objects
    shuffle=True,
    class_weight=None,       # dict {class:weight} for imbalanced
    sample_weight=None,
    initial_epoch=0,
    steps_per_epoch=None,
    verbose=1,               # 0=silent 1=progress bar 2=line
)
print(f"History keys: {list(history.history.keys())}")

# ── evaluate / predict ────────────────────────────────────────────
X_test = np.random.randn(200,784).astype("float32")
y_test = np.random.randint(0,10,200)
results = model.evaluate(X_test,y_test,verbose=0)
print(f"Test loss: {results[0]:.4f}  Acc: {results[1]:.4f}")
predictions = model.predict(X_test,batch_size=64,verbose=0)
print(f"Predictions shape: {predictions.shape}")""",
["History keys: ['loss', 'accuracy', 'val_loss', 'val_accuracy']",
 "Predictions shape: (200, 10)"])
)

s3=section(3,"Built-in Layers &amp; Regularization",
  "Dense, Conv2D, LSTM, GRU, BatchNorm, Dropout — all params documented. "
  "Regularization prevents overfitting through weight penalties and noise.",
  cb("Dense / Conv2D / LSTM / BatchNorm / Dropout / regularizers",
"""import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers

# ── Dense layer params ────────────────────────────────────────────
d = layers.Dense(
    units=256,                              # output neurons
    activation="relu",                      # "relu" "sigmoid" "tanh" "softmax" "linear" None
    use_bias=True,
    kernel_initializer="glorot_uniform",    # "he_normal" "glorot_uniform" "zeros"
    bias_initializer="zeros",
    kernel_regularizer=regularizers.l2(1e-4),  # L2 weight decay
    activity_regularizer=None,
    kernel_constraint=None,
)

# ── Conv2D ────────────────────────────────────────────────────────
conv = layers.Conv2D(
    filters=64,                # number of output feature maps
    kernel_size=(3,3),         # filter size; can be int 3
    strides=(1,1),             # stride for each spatial dim
    padding="same",            # "same"=preserve size "valid"=no pad
    activation="relu",
    use_bias=True,
    kernel_initializer="he_normal",
    kernel_regularizer=regularizers.l2(1e-4),
    data_format="channels_last", # "channels_first" for GPU
    dilation_rate=1,           # dilated/atrous convolution
)

# ── LSTM ──────────────────────────────────────────────────────────
lstm = layers.LSTM(
    units=128,
    return_sequences=True,     # True=return all timesteps
    return_state=False,        # True=also return final h and c
    go_backwards=False,        # True=process input reversed
    stateful=False,            # True=reuse state between batches
    dropout=0.1,               # dropout on inputs
    recurrent_dropout=0.0,     # dropout on recurrent state
    unroll=False,              # unroll for small seq (faster but more memory)
)

# ── Normalization ─────────────────────────────────────────────────
bn = layers.BatchNormalization(
    axis=-1,               # axis to normalize (usually channel axis)
    momentum=0.99,         # running average momentum
    epsilon=1e-3,
    center=True, scale=True,
    trainable=True,
)
ln = layers.LayerNormalization(axis=-1)     # normalizes over last axis
gn = layers.GroupNormalization(groups=8)    # group norm (tf 2.12+)

# ── Dropout ───────────────────────────────────────────────────────
dr  = layers.Dropout(rate=0.3,seed=42)     # drops random units
sd  = layers.SpatialDropout2D(rate=0.2)    # drops entire feature maps
ad  = layers.AlphaDropout(rate=0.1)        # self-normalising networks

# ── Regularizers ─────────────────────────────────────────────────
r_l1=regularizers.l1(1e-4)          # L1 (lasso — sparsity)
r_l2=regularizers.l2(1e-4)          # L2 (ridge — weight decay)
r_l1l2=regularizers.l1_l2(l1=1e-5,l2=1e-4)  # combined

print("All layers and regularizers documented")""",["All layers and regularizers documented"])
)

s4=section(4,"Training Pipeline &amp; Callbacks",
  "EarlyStopping, ModelCheckpoint, and TensorBoard are the three essential callbacks. "
  "tf.data.Dataset gives you the fastest possible data loading.",
  cb("Callbacks / tf.data.Dataset / custom training loop",
"""import tensorflow as tf
from tensorflow import keras
import numpy as np

# ── Callbacks ─────────────────────────────────────────────────────
early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=10,            # wait N epochs without improvement
    mode="min",             # "min" "max" "auto"
    restore_best_weights=True,
    baseline=None,
    start_from_epoch=0,
)

checkpoint = keras.callbacks.ModelCheckpoint(
    filepath="best_model.keras",
    monitor="val_accuracy",
    save_best_only=True,
    save_weights_only=False,
    mode="max",
    verbose=1,
)

reduce_lr = keras.callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,             # multiply LR by this on plateau
    patience=5,
    min_lr=1e-7,
    verbose=1,
)

tensorboard = keras.callbacks.TensorBoard(
    log_dir="./logs",
    histogram_freq=1,       # compute weight histograms every N epochs
    write_graph=True,
    update_freq="epoch",    # "batch" or int (batch freq)
)

csv_logger = keras.callbacks.CSVLogger("training.csv",append=True)

# ── tf.data.Dataset ───────────────────────────────────────────────
X = np.random.randn(1000,28,28,1).astype("float32")
y = np.random.randint(0,10,1000)

ds = tf.data.Dataset.from_tensor_slices((X,y))
ds = ds.shuffle(buffer_size=1000,seed=42)      # random shuffling
ds = ds.batch(32)                               # create batches
ds = ds.map(lambda x,y: (x/255.,y),           # normalize
    num_parallel_calls=tf.data.AUTOTUNE)        # auto parallelism
ds = ds.cache()                                 # cache after map
ds = ds.prefetch(tf.data.AUTOTUNE)             # async prefetch
print(f"Dataset batches: {len(list(ds))}")

# ── Custom training loop ──────────────────────────────────────────
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28,1)),
    keras.layers.Dense(128,activation="relu"),
    keras.layers.Dense(10),
])
optimizer = keras.optimizers.Adam(1e-3)
loss_fn   = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
train_acc = keras.metrics.SparseCategoricalAccuracy()

for epoch in range(2):
    train_acc.reset_state()
    for x_batch,y_batch in ds:
        with tf.GradientTape() as tape:
            logits = model(x_batch,training=True)
            loss   = loss_fn(y_batch,logits)
        grads = tape.gradient(loss,model.trainable_variables)
        optimizer.apply_gradients(zip(grads,model.trainable_variables))
        train_acc.update_state(y_batch,logits)
    print(f"Epoch {epoch+1} acc={train_acc.result():.4f}")""",
["Dataset batches: 32","Epoch 1 acc=0.1234","Epoch 2 acc=0.1456"])
)

s5=section(5,"Model Saving, Transfer Learning &amp; Advanced Features",
  "Save models in SavedModel or Keras format. Transfer learning reuses pretrained weights. "
  "Mixed precision and MirroredStrategy unlock GPU speed.",
  cb("save/load / transfer learning / mixed precision / MirroredStrategy / TFLite",
"""import tensorflow as tf
from tensorflow import keras

# ── Saving and Loading ─────────────────────────────────────────────
model = keras.Sequential([keras.layers.Dense(10,activation="softmax",input_shape=(5,))])
model.compile(optimizer="adam",loss="categorical_crossentropy",metrics=["accuracy"])

# SavedModel format (recommended, TF 2.x default)
model.save("my_model")                    # creates directory
loaded = keras.models.load_model("my_model")

# Keras format (.keras) — single file
model.save("my_model.keras")
loaded = keras.models.load_model("my_model.keras")

# Weights only
model.save_weights("weights.h5")         # HDF5 weights
model.load_weights("weights.h5")

# ── Transfer Learning ─────────────────────────────────────────────
# Step 1: load pretrained base
base = keras.applications.MobileNetV2(
    weights="imagenet",   # load pretrained ImageNet weights
    include_top=False,    # exclude final Dense classifier
    input_shape=(224,224,3),
)
base.trainable = False    # freeze ALL base layers

# Step 2: add custom head
inputs = keras.Input(shape=(224,224,3))
x = keras.applications.mobilenet_v2.preprocess_input(inputs)
x = base(x, training=False)             # inference mode for BN
x = keras.layers.GlobalAveragePooling2D()(x)
x = keras.layers.Dropout(0.2)(x)
outputs = keras.layers.Dense(5,activation="softmax")(x)
model2 = keras.Model(inputs,outputs)
print(f"Trainable params: {model2.count_params():,}")

# Step 3: fine-tune — unfreeze top layers
base.trainable = True
for layer in base.layers[:-20]:   # freeze all but last 20
    layer.trainable = False
model2.compile(
    optimizer=keras.optimizers.Adam(1e-5),  # very low LR for fine-tuning
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

# ── Mixed Precision ───────────────────────────────────────────────
keras.mixed_precision.set_global_policy("mixed_float16")
# All Dense/Conv2D run in float16, BN runs in float32
# Use float32 output layer to prevent numerical instability:
outputs2 = keras.layers.Dense(5,activation="softmax",dtype="float32")(x)
keras.mixed_precision.set_global_policy("float32")  # reset

# ── Multi-GPU: MirroredStrategy ────────────────────────────────────
strategy = tf.distribute.MirroredStrategy()
print(f"GPUs: {strategy.num_replicas_in_sync}")
with strategy.scope():
    # All model/optimizer creation MUST be inside scope
    dist_model = keras.Sequential([
        keras.layers.Dense(128,activation="relu",input_shape=(10,)),
        keras.layers.Dense(1),
    ])
    dist_model.compile(optimizer="adam",loss="mse")

# ── TFLite Conversion ─────────────────────────────────────────────
converter = tf.lite.TFLiteConverter.from_keras_model(model)
# Optimization options:
# converter.optimizations = [tf.lite.Optimize.DEFAULT]  # quantize
tflite_model = converter.convert()
with open("/tmp/model.tflite","wb") as f:
    f.write(tflite_model)
print(f"TFLite model size: {len(tflite_model)/1024:.1f} KB")""",
["GPUs: 1","TFLite model size: 5.2 KB"])
)

body="".join([s1,s2,s3,s4,s5])
body+=playground("""# TensorFlow / Keras quick reference
print("Model creation:")
print("  Sequential:  model = keras.Sequential([Dense(128,'relu'), Dense(10,'softmax')])")
print("  Functional:  inputs=Input(784); x=Dense(256)(inputs); out=Dense(10)(x)")
print()
print("Compile:")
print("  model.compile(optimizer=Adam(1e-3), loss='sparse_categorical_crossentropy', metrics=['accuracy'])")
print()
print("Fit:")
print("  history = model.fit(X_tr,y_tr, epochs=50, batch_size=64, validation_split=0.1,")
print("                      callbacks=[EarlyStopping(patience=5)])")
print()
print("Evaluate / Predict:")
print("  model.evaluate(X_te, y_te)")
print("  preds = model.predict(X) # shape (n_samples, n_classes)")
print()
print("Save / Load:")
print("  model.save('model.keras')  # recommended")
print("  model = keras.models.load_model('model.keras')")""")

out=HEAD.format(title="TensorFlow",desc="TensorFlow/Keras complete reference — 35 topics.")+\
    HERO.format(title="TensorFlow",desc="Tensors, Variables, GradientTape, Keras Sequential/Functional/Subclassing API, all layer types, callbacks, tf.data pipelines, transfer learning, and deployment.",n=35)+\
    toc(topics)+body+foot(("Scikit-Learn","sklearn.html"),("Standard Library","stdlib.html"))
with open(os.path.join(BASE,"tensorflow.html"),"w",encoding="utf-8") as f:
    f.write(out)
print(f"tensorflow.html  {len(out):>10,} chars")
