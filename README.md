# vits-preprocessing
script to pre-process audio files to train vits in spanish
## Tested in python 3.10.13
### this scripts as it is only works for spanish, though it can be easly converted to work with over a 100 different languages.
### How to use it:
#### Install all dependencies:
* `pip install -r requirements.txt`
* #### Install [Espeak](https://github.com/espeak-ng/espeak-ng)
*   ```
    #Install Cython-version Monotonoic Alignment Search 
    cd monotonic_align
    python setup.py build_ext --inplace
    ```
#### Run the program:
* Generate the audio files and transcriptions
    `python gen_data.py --target_sr 22500 --output_dir dataset --audio_dir audio`
    --target_sr: Set the target sampling rate (default is 22500).
    --output_dir: Specify the directory for files generated by the script (default is 'dataset').
    --audio_dir: Specify the directory containing audio files (default is 'audio').
 * Split the data into training and test data
 `python script.py --train_size 90 --test_size 10 --data_dir dataset`
    --train_size: Set the percentage of data for training (default is 90%).
    --test_size: Set the percentage of data for testing (default is 10%).
    --data_dir: Specify the directory containing the generated data (should be the same as output_dir in the gen_data.py script).
* Clean the text and generate the phenomizer
`python text.py --data_dir dataset`
    --data_dir: Specify the directory containing the generated data (should be the same as output_dir in the gen_data.py script).
