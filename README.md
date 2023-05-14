# Music-Generation
Music Generation Research Project

## Purpose

The purpose of this project is to explore various methods using Machine Learning and Neural Networks to generate the best sounding music possible. Artifical intelligence has expanded to the realms of art and writing, but there are few tools focusing on music generation. 

## Literature Review

I found that most previous attempts at music generation use simple RNNs or LSTMs. My intial research question was if it was possible to use convolutional neural networks to convolve over piano roll representations of music in order to capture both melodic and chordal information at the same time. There was one paper that was published that I found that used CNN architecture, this is called [MidiNet](https://github.com/RichardYang40148/MidiNet/tree/master/v1). This is similar to what I was thinking of during my intial drafting of my research question.

## Data
The dataset I used for testing purposes for this project can be found [here](https://www.kaggle.com/datasets/soumikrakshit/classical-music-midi). It consists of 295 MIDI files from 19 different classical composers of various eras. The tempo varies considerably, as well as musical style. However, these are all piano pieces, so other instruments are not present in these songs. 

## Methodology
In order to begin analysis of the broad features present in music, I began by creating a simple probabilistic based model. In order to read midi files, I used the library [mido](https://mido.readthedocs.io/en/latest/). I built various functions in order to convert a midi file into several different forms. The main form that was intially used was a simple string of "notes". These notes are represented as numbers from 21 to 109, or the 88 notes present on a piano. It should be noted that I pulled the note values into an array, this means that any vertical features in the music were lost, as the notes present are represented in a one dimensional array. 

We began our exploration by building a simple N-gram model. I encounted a few difficulties in this because, most statastical libraries, such as scikit-learn, expext the input format for an N-gram model to be of type string, rather than our representation of and integer. Intially, I only used one song, **Mary had a little lamb** as our intial piece of test music. I built a simple N-gram model by hand, and generated music using only note data, time data (or the note length) and volume data was not included.

This produced somewhat coherent results, however, given that we were only sampling from one song, this was be to expected because every N-gram the model could choose was in the same key, and since the tempo was constast, there were no large fluctuations in tempo.

After intial success, we extended the probabilistic model to pull from a corpus containing the "note-arrays" of all 295 MIDI files we had. I created a small csv file which has the file name, composer name, and "note-array". We then built several different models for generation from this corpus, which can be found in the "Generated_Music" folder. We attempted a 5-gram and 15-gram models, which produced decent results. 

The next step was to introduce tempo into our model. Intially, we just created two different arrays, a "note-array" and "tempo-array", then generated from both in parallel. This produced mostly incoherent results, and it seems we need to reevaluate how we are to combine time and note data into our model.

## Tentative Results

While the music that was created wasn't perfect, or even close to human-created music, it did raise the question, can NLP techniques be used for this project? By using an N-gram model and getting somewhat coherent results, this opens the door to perhaps retrofitting other NLP techniques and using them for this purpose. For example, we could potentially use a CNN and an enconder-decoder architecture for this project. 


## Future Work

The next steps of this project are:
- Create a databse for our music corpus, this will contain metadata, as well as the MIDI files we will use
- Properly format the data; as of now, we are losing the vertical nature of the music due to the array like nature of how we are handling it. We need to find a way to convert it into some form of 2 or higher dimensional representation.
- Finish proabilistic modeling and simple testing
- Attempt to recreate both RNN and CNN generational techniques used in the past
- Create our own deep-learning based approach, which will be based on MIDI

This is where the project will become significantly more difficult. I hope to perhaps explore using natural language processing techniques, as well as recreate what has been done in the past with RNNs. If I am to continue in the fall, I will attempt to incoorporate many different deep-learning techniques, as I believe this is the natural next step for this project.



