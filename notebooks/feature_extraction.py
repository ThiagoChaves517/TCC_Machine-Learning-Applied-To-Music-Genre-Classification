import librosa
import numpy as np
import pandas as pd

def extract_features(file_path):
    try:
        # Carrega o áudio: mono=True, sr=None (mantém a taxa original)
        # O utils.py do FMA usa sr=None
        wave_form_y, sampling_rate = librosa.load(file_path, mono=True, sr=None)
        
        features = {}
        
        # Extrai features (exemplos)
        mfcc = librosa.feature.mfcc(y=wave_form_y, sr=sampling_rate, n_mfcc=20)
        spectral_contrast = librosa.feature.spectral_contrast(y=wave_form_y, sr=sampling_rate)
        chroma = librosa.feature.chroma_cens(y=wave_form_y, sr=sampling_rate)
        zcr = librosa.feature.zero_crossing_rate(wave_form_y)
        
        # Agrega features com estatísticas (como em features.py)
        # Para cada feature, calcule média, std, mediana, etc.
        features['mfcc_mean'] = np.mean(mfcc, axis=1)
        features['mfcc_std'] = np.std(mfcc, axis=1)
        
        features['contrast_mean'] = np.mean(spectral_contrast, axis=1)
        features['contrast_std'] = np.std(spectral_contrast, axis=1)
        
        features['chroma_mean'] = np.mean(chroma, axis=1)
        features['chroma_std'] = np.std(chroma, axis=1)
        
        features['zcr_mean'] = np.mean(zcr)
        features['zcr_std'] = np.std(zcr)
        
        # Achata todos os arrays em um único vetor
        # É importante que todos os vetores tenham o mesmo comprimento e ordem
        all_features = np.hstack([
            features['mfcc_mean'], features['mfcc_std'],
            features['contrast_mean'], features['contrast_std'],
            features['chroma_mean'], features['chroma_std'],
            features['zcr_mean'], features['zcr_std']
        ])
        
        return all_features
        
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return None
    
def get_column_names():
    """Gera uma lista de nomes de colunas na ordem correta da extração."""
    column_names = []
    
    n_mfcc = 20
    n_contrast = 7
    n_chroma = 12
    
    # 1. MFCC Mean & Std
    column_names.extend([f'mfcc_mean_{i+1:02d}' for i in range(n_mfcc)])
    column_names.extend([f'mfcc_std_{i+1:02d}' for i in range(n_mfcc)])
    
    # 2. Spectral Contrast Mean & Std
    column_names.extend([f'contrast_mean_{i+1:02d}' for i in range(n_contrast)])
    column_names.extend([f'contrast_std_{i+1:02d}' for i in range(n_contrast)])
    
    # 3. Chroma Mean & Std
    column_names.extend([f'chroma_mean_{i+1:02d}' for i in range(n_chroma)])
    column_names.extend([f'chroma_std_{i+1:02d}' for i in range(n_chroma)])
    
    # 4. ZCR Mean & Std
    column_names.append('zcr_mean_01')
    column_names.append('zcr_std_01')
    
    return column_names