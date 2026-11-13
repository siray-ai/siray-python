"""Example: Audio/music generation using Siray SDK."""

from siray import Siray, SirayError


client = Siray()  # Uses SIRAY_API_KEY from environment


def example_audio_generation():
    """Generate a song with lyrics."""
    print("=== Audio Generation ===")

    try:
        response = client.audio.generate_async(
            model="minimax/music-3.0",
            prompt=(
                "Cinematic pop song with an emotional female lead vocal, "
                "warm piano, atmospheric synth pads and a powerful chorus"
            ),
            lyrics=(
                "[Verse]\nI left the light on by the door\n"
                "Like you might come back once more\n\n"
                "[Chorus]\nIf the city falls asleep tonight\n"
                "I'll keep running toward the light"
            ),
            lyrics_optimizer=False,
            is_instrumental=False,
            bitrate=256000,
            sample_rate=44100,
        )

        print("Audio generation started!")
        print(f"Task ID: {response.task_id}")

    except SirayError as e:
        print(f"Error: {e.message}")


def example_instrumental_generation():
    """Generate instrumental music, letting the model create lyrics structure."""
    print("\n=== Instrumental Audio Generation ===")

    try:
        status = client.audio.run(
            model="minimax/music-3.0",
            prompt="Warm cinematic instrumental pop with piano and strings",
            lyrics_optimizer=True,
            is_instrumental=True,
            bitrate=256000,
            sample_rate=44100,
            poll_interval=3.0,
            timeout=10 * 60,
        )

        if status.is_completed():
            print(f"Generated audio: {status.result}")
            print(f"All outputs: {status.outputs}")
        elif status.is_failed():
            print(f"Error: {status.fail_reason}")

    except (SirayError, TimeoutError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    example_audio_generation()
    example_instrumental_generation()
