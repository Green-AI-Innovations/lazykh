# use this code outside this container to save space 

#add this to requirments.txt
# torch==1.9.0
# torchaudio==0.9.0
# fairseq
# huggingface_hub
# g2p_en

# import torch
# import torchaudio
# from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
# from fairseq.models.text_to_speech.hub_interface import TTSHubInterface


# def text_to_speech(text: str, wav_file_path: str) -> None:
#     # Load model ensemble and task from Hugging Face Hub
#     models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
#         "facebook/fastspeech2-en-ljspeech",
#         arg_overrides={
#             "vocoder": "hifigan",
#             "fp16": False,
#             "cpu": True,
#         },
#     )
#     model = models[0]

#     # Update configuration with data configuration
#     TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)

#     device = torch.device("cpu")
#     model.to(device)  # Move the model to the device

#     # Build generator
#     generator = task.build_generator([model], cfg)

#     # Get model input
#     sample = TTSHubInterface.get_model_input(task, text)
#     sample["net_input"]["src_tokens"] = sample["net_input"]["src_tokens"].to(device)
#     sample["net_input"]["src_lengths"] = sample["net_input"]["src_lengths"].to(device)
#     sample["speaker"] = (
#         sample["speaker"].to(device)
#         if sample["speaker"] is not None
#         else torch.tensor([[0]]).to(device)
#     )

#     # Get prediction
#     wav, rate = TTSHubInterface.get_prediction(task, model, generator, sample)

#     wav_2d = wav.unsqueeze(0)
#     torchaudio.save(
#         wav_file_path,
#         wav_2d,
#         sample_rate=rate,
#         channels_first=True,
#         format="wav",
#         encoding="PCM_S",
#         bits_per_sample=16,
#     )
