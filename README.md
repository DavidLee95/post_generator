# Post Generator

**Post Generator** is a Python program that helps you instantly create beautiful Instagram posts based on a phrase, logo, and handle provided by the user. Whether you're running a personal brand or a business account, this tool can help you create aesthetic, shareable content in seconds.

## 📌 Features

- Accepts custom phrases to be displayed on Instagram posts.
- Optionally supports uploading a logo and Instagram handle.
- Uses a set of 20 background images to be used to generate the posts.
- Matches each phrase with a corresponding background image to generate polished posts.
- Generates up to 20 unique posts based on the user's phrases, logo, and handle.

## ⚙️ Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/post-generator.git
   cd_post-generator
   ```

2. **Install dependencies** 
It's recommended to use a virtual environment.
     ```bash
     pip install -r requirements.txt
     ```

## 🚀 Usage


## 🛠 Tech Stack
* Language: Python
* Libraries: Pillow, os

## 📁 How It Works
1. Go to the file named "phrases.txt", in which there is one phrase per line.

2. Fill up to 20 phrases that you wish to use to generate your Instagram posts.

3. When the program runs:

  * It prompts you to enter the number of posts to generate (must be at most 20).

  * This number must equal the number of phrases in phrases.txt.

  * Each phrase is paired with a corresponding image from the images located in the "background_images" folder.

4. The program generates Instagram-ready posts using the provided text and optional logo/handle, which will be saved in the "generated_posts" folder.

## 🧑‍💻 Contributing
Pull requests are welcome! If you'd like to improve the project, feel free to fork it and submit a PR. Please make sure your contributions follow best practices and are well-tested.

## 📄 License
This project is under the terms of the [MIT license](https://opensource.org/license/mit/).
