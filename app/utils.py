import os
import requests
from flask import current_app

def process_image_external(image_path):
    """
    Sends the uploaded image to an external conversion server.
    Expects a JSON response with an 'output_filename' field.
    """
    from flask import current_app

    conversion_url = current_app.config.get("CONVERSION_SERVER_URL")
    if not conversion_url:
        raise Exception("Conversion server URL not configured.")

    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(conversion_url, files=files, timeout=60)

    if response.status_code == 200:
        data = response.json()
        output_filename = data.get("output_filename")
        if output_filename:
            return output_filename
        else:
            raise Exception("Conversion server did not return output filename.")
    else:
        raise Exception(f"Conversion server returned status {response.status_code}")

def image_gen_replica(image_path):
    import replicate
    import os
    import base64

    input_filename = image_path.split("/")[-1]
    with open(image_path, 'rb') as file:
        data = base64.b64encode(file.read()).decode('utf-8')
        image = f"data:application/octet-stream;base64,{data}"

    input = {
        "image": image,
        "prompt": "A beautifully detailed anime scene in the iconic Studio Ghibli style, featuring soft, hand-painted backgrounds with rich natural elements like lush green forests, rolling hills, and a dreamy sky filled with fluffy clouds. The lighting is warm and golden, evoking a nostalgic and magical atmosphere. The characters have expressive, youthful faces with large, soulful eyes and simple, clean features. They wear whimsical, slightly old-fashioned clothing with earthy or pastel tones, moving through a serene, slightly fantastical countryside village. Small, imaginative details abound — soot sprites hiding in corners, oversized plants, rustic cottages with moss-covered roofs, mysterious spirits lurking in the shadows, and gentle wind rustling through tall grass. The environment feels alive and gently surreal, blending elements of everyday life with quiet magic. The entire composition has a painterly, storybook quality, with a focus on emotion, nature, and wonder — reminiscent of My Neighbor Totoro, Spirited Away, and Howl's Moving Castle. Soft shadows, gentle color palettes, and a touch of whimsy complete the scene.",
        "lora_scale": 0.85,
        "output_format": "jpg",
        "output_quality": 100,
        "prompt_strength": 0.57,
        "num_inference_steps": 12,
        "guidance_scale": 9,
    }
    #print("input:", input)

    output = replicate.run(
        "colinmcdonnell22/ghiblify-3:407b7fd425e00eedefe7db3041662a36a126f1e4988e6fbadfc49b157159f015",
        input=input
    )
    print("output:", output)
    output_path = os.path.join(current_app.config['PRODUCT_FOLDER'], input_filename)
    for index, item in enumerate(output):
        with open(output_path, "wb") as file:
            file.write(item.read())
    # => output_0.jpg written to disk
    return output_path