
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

That model only ended up giving me accuracy of around 0.103
After doing some research, I added two more convolution layers to 
detect the details of the images, added more filters for each layer, and lowered the dropout rate. After lowering the dropout rate to 0.3, and increases the filters, the model performed extremely well, with an accuracy of 0.9896. 

I noticed that if there is more detail in the images, there needs
to be more convolution layers. I also learned that if the dataset
is relatively small, like this one, you shouldn't use a high dropout rate. 