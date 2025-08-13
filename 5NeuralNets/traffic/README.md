
Seeing that the example network for the handwritten digits had 
- 1 Convolution + Pooling cycle, 
    - 2x2 Pools
- 1 Hidden Layer with Dropout
    - 128 Units
    - Dropout at 0.5
- 1 output layer with 10 units and softmax activation

I wanted to start with something similar but a little more robust due to the
amount of different classifications that had to be made. Knowing that the images were 30x30, 
I didn't want to make the pools too small so that the model could detect differences in similar signs. 
I also knew I needed at least one more hidden layer but with perhaps less nodes. 
My first model was
- 1 Convolution + Pooling cycle, 
    - 2x2 Pools
- 2 Hidden Layers with Dropout
    - 16 Units Each
    - Dropout out 0.5
- 1 output layer with 43 units


This ended giving me accuracy of 0.0554 and loss of 3.4969. 
This model evidently was not large enough to make solid predictions and was only a little better than random guessing. 
I am going to add another hidden layers with Dropout and extend each hidden layer to be 64 units each. I am also going to add another convolution and pooling cycle and increase the filters in each layer from 32 to 64