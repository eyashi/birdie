import numpy as np
import librosa
import os
from sklearn import preprocessing

def load_audio(filename, mono=True, fs=22050):
    """Load audio file into numpy array
    Supports 24-bit wav-format
    
    Taken from TUT-SED system: https://github.com/TUT-ARG/DCASE2016-baseline-system-python
    
    Parameters
    ----------
    filename:  str
        Path to audio file

    mono : bool
        In case of multi-channel audio, channels are averaged into single channel.
        (Default value=True)

    fs : int > 0 [scalar]
        Target sample rate, if input audio does not fulfil this, audio is resampled.
        (Default value=44100)

    Returns
    -------
    audio_data : numpy.ndarray [shape=(signal_length, channel)]
        Audio

    sample_rate : integer
        Sample rate

    """

    file_base, file_extension = os.path.splitext(filename)
    if file_extension == '.wav' or file_extension == '.mp3':
        return librosa.load(filename)

    elif file_extension == '.npy':
        sound_arr = numpy.load(filename)
        sample_rate = fs
        
        return sound_arr, sample_rate

    return None, None


def load_desc_file(_desc_file):
    _desc_dict = dict()
    for line in open(_desc_file):
        words = line.strip().split('\t')
        name = words[0].split('/')[-1]
        if name not in _desc_dict:
            _desc_dict[name] = list()
        _desc_dict[name].append([float(words[2]), float(words[3]), __class_labels[words[-1]]])
    return _desc_dict


def extract_mbe(_y, _sr, _nfft, _nb_mel):
    spec, n_fft = librosa.core.spectrum._spectrogram(y=_y, n_fft=_nfft, hop_length=_nfft/2, power=1)
    mel_basis = librosa.filters.mel(sr=_sr, n_fft=_nfft, n_mels=_nb_mel)
    return np.log(np.dot(mel_basis, spec))

# ###################################################################
#              Main script starts here
# ###################################################################

is_mono = True

# location of data.
evaluation_setup_folder = 'eval'
audio_folder = 'samples'

# Output
feat_folder = 'feat'

# User set parameters
nfft = 2048
win_len = nfft
hop_len = win_len / 2
nb_mel_bands = 40
sr = 22050

# -----------------------------------------------------------------------
# Feature extraction and label generation
# -----------------------------------------------------------------------
# Load labels
train_file = os.path.join(evaluation_setup_folder, 'street_fold{}_train.txt'.format(1))
evaluate_file = os.path.join(evaluation_setup_folder, 'street_fold{}_evaluate.txt'.format(1))
desc_dict = load_desc_file(train_file)
desc_dict.update(load_desc_file(evaluate_file)) # contains labels for all the audio in the dataset

# Extract features for all audio files, and save it along with labels
for audio_filename in os.listdir(audio_folder):
    audio_file = os.path.join(audio_folder, audio_filename)
    print('Extracting features and label for : {}'.format(audio_file))
    y, sr = load_audio(audio_file, mono=is_mono, fs=sr)
    mbe = None

    if is_mono:
        mbe = extract_mbe(y, sr, nfft, nb_mel_bands).T
    else:
        for ch in range(y.shape[0]):
            mbe_ch = extract_mbe(y[ch, :], sr, nfft, nb_mel_bands).T
            if mbe is None:
                mbe = mbe_ch
            else:
                mbe = np.concatenate((mbe, mbe_ch), 1)

    label = np.zeros((mbe.shape[0], len(__class_labels)))
    tmp_data = np.array(desc_dict[audio_filename])
    frame_start = np.floor(tmp_data[:, 0] * sr / hop_len).astype(int)
    frame_end = np.ceil(tmp_data[:, 1] * sr / hop_len).astype(int)
    se_class = tmp_data[:, 2].astype(int)
    for ind, val in enumerate(se_class):
        label[frame_start[ind]:frame_end[ind], val] = 1
    tmp_feat_file = os.path.join(feat_folder, '{}_{}.npz'.format(audio_filename, 'mon' if is_mono else 'bin'))
    np.savez(tmp_feat_file, mbe, label)

# -----------------------------------------------------------------------
# Feature Normalization
# -----------------------------------------------------------------------

# use os.listdir instead
for fold in folds_list:
    train_file = os.path.join(evaluation_setup_folder, 'street_fold{}_train.txt'.format(1))
    evaluate_file = os.path.join(evaluation_setup_folder, 'street_fold{}_evaluate.txt'.format(1))
    train_dict = load_desc_file(train_file)
    test_dict = load_desc_file(evaluate_file)

    X_train, Y_train, X_test, Y_test = None, None, None, None
    for key in train_dict.keys():
        tmp_feat_file = os.path.join(feat_folder, '{}_{}.npz'.format(key, 'mon' if is_mono else 'bin'))
        dmp = np.load(tmp_feat_file)
        tmp_mbe, tmp_label = dmp['arr_0'], dmp['arr_1']
        if X_train is None:
            X_train, Y_train = tmp_mbe, tmp_label
        else:
            X_train, Y_train = np.concatenate((X_train, tmp_mbe), 0), np.concatenate((Y_train, tmp_label), 0)

    for key in test_dict.keys():
        tmp_feat_file = os.path.join(feat_folder, '{}_{}.npz'.format(key, 'mon' if is_mono else 'bin'))
        dmp = np.load(tmp_feat_file)
        tmp_mbe, tmp_label = dmp['arr_0'], dmp['arr_1']
        if X_test is None:
            X_test, Y_test = tmp_mbe, tmp_label
        else:
            X_test, Y_test = np.concatenate((X_test, tmp_mbe), 0), np.concatenate((Y_test, tmp_label), 0)

    # Normalize the training data, and scale the testing data using the training data weights
    scaler = preprocessing.StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    normalized_feat_file = os.path.join(feat_folder, 'mbe_{}_fold{}.npz'.format('mon' if is_mono else 'bin', fold))
    np.savez(normalized_feat_file, X_train, Y_train, X_test, Y_test)
    print('normalized_feat_file : {}'.format(normalized_feat_file))




