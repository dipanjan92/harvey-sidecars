import argparse
import os
import sys
import torch
from pyannote.audio import Pipeline
from transformers import MarianMTModel, MarianTokenizer, pipeline as hf_pipeline

# === Configure Matplotlib to use bundled font cache ===
# This is necessary for pyannote.audio to work correctly when bundled with PyInstaller
def _get_resource_root():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(__file__)

# Point MPLCONFIGDIR to the embedded .matplotlib folder
base_path = _get_resource_root()
mpl_cache = os.path.join(base_path, 'resources', '.matplotlib')
os.environ['MPLCONFIGDIR'] = mpl_cache

def get_model_cache():
    """
    Determine the path to the bundled `models` folder.
    When running as a PyInstaller onefile executable, resources are unpacked to sys._MEIPASS.
    Otherwise, use the script's `models/` directory alongside it.
    """
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'models')
    return os.path.join(os.path.dirname(__file__), 'models')

def run_diarization(args):
    """
    Performs speaker diarization on an audio file.
    """
    print("Running diarization...")

    # Force HF Hub fully offline
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"

    # Locate bundled models cache
    model_cache = get_model_cache()
    if not os.path.isdir(model_cache):
        sys.exit(f"Error: bundled models directory not found at {model_cache}")

    # Load the diarization pipeline from local cache
    diarization_pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=False,
        cache_dir=model_cache
    )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    diarization_pipeline.to(device)

    # Build optional diarization parameters
    kwargs = {}
    if args.num_speakers is not None and args.num_speakers > 0:
        kwargs["num_speakers"] = args.num_speakers
    if hasattr(args, 'min_speakers') and args.min_speakers is not None:
        kwargs["min_speakers"] = args.min_speakers
    if hasattr(args, 'max_speakers') and args.max_speakers is not None:
        kwargs["max_speakers"] = args.max_speakers

    # Run diarization and write output to RTTM
    diarization = diarization_pipeline(args.audio, **kwargs)
    with open(args.output, "w") as f:
        diarization.write_rttm(f)

    print(f"Finished diarization. Result saved to {args.output}")


def run_translation(args):
    """
    Translates text from a source language to a target language.
    """
    print("Running translation...")

    # A simple mapping for supported language pairs to model names
    model_mapping = {
        "en-ja": "Helsinki-NLP/opus-mt-en-jap",
        "ja-en": "Helsinki-NLP/opus-mt-ja-en",
    }

    lang_pair = f"{args.from_lang}-{args.to}"
    if lang_pair not in model_mapping:
        print(f"Error: Translation from '{args.from_lang}' to '{args.to}' is not supported.")
        sys.exit(1)

    model_name = model_mapping[lang_pair]
    
    custom_model_path = os.path.abspath(args.model_path)
    
    config_path = os.path.join(custom_model_path, 'config.json')
    if not os.path.exists(config_path):
        print(f"Error: Model not found at '{custom_model_path}'. Please download the model first.")
        sys.exit(1)
    else:
        print(f"Model '{model_name}' already exists at '{custom_model_path}'.")

    translator = hf_pipeline(f"translation_{args.from_lang}_to_{args.to}", model=custom_model_path)
    translated_text = translator(args.text)
    print(f"Translated text: {translated_text[0]['translation_text']}")


def main():
    parser = argparse.ArgumentParser(description="A command-line tool for diarization and translation.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Diarization sub-command
    diarize_parser = subparsers.add_parser("diarize", help="Perform speaker diarization on an audio file.")
    diarize_parser.add_argument("--audio", type=str, required=True, help="Path to the audio file.")
    diarize_parser.add_argument("--output", type=str, default="output.rttm", help="Path to save the RTTM file.")
    diarize_parser.add_argument("--num_speakers", type=int, default=0, help="Number of speakers. If 0, it will be detected automatically.")
    diarize_parser.add_argument("--min_speakers", type=int, help="Minimum number of speakers")
    diarize_parser.add_argument("--max_speakers", type=int, help="Maximum number of speakers")
    diarize_parser.set_defaults(func=run_diarization)

    # Translation sub-command
    translate_parser = subparsers.add_parser("translate", help="Translate text from one language to another.")
    translate_parser.add_argument("--text", type=str, required=True, help="The text to translate.")
    translate_parser.add_argument("--from", type=str, required=True, help="The source language (e.g., 'en').", dest='from_lang')
    translate_parser.add_argument("--to", type=str, required=True, help="The target language (e.g., 'ja').")
    translate_parser.add_argument("--model-path", type=str, required=True, help="Path to the translation model directory.")
    translate_parser.set_defaults(func=run_translation)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()