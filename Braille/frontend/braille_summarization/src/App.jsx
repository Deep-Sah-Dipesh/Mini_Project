import React, { useState } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [caption, setCaption] = useState("");
  const [braille, setBraille] = useState("");
  const [error, setError] = useState("");

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result.split(",")[1]); 
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async () => {
    if (!image) {
      setError("Please upload an image!");
      return;
    }

    setError("");
    try {
      const response = await fetch("http://127.0.0.1:5000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image }), 
      });

      const data = await response.json();
      if (response.ok) {
        setCaption(data.caption);
        setBraille(data.braille);
      } else {
        setError(data.error || "Something went wrong!");
      }
    } catch (err) {
      setError("Failed to connect to the server!");
    }
  };

  return (
    <div className="App">
      <header>
        <h1>Image Summarization and Braille Conversion</h1>
        <p>Upload an image to generate its caption and Braille text representation.</p>
      </header>

      <main>
        <section className="upload-section">
          <h2>Upload Any Image</h2>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
          />
          {imagePreview && (
            <div className="image-preview">
              <img src={imagePreview} alt="Uploaded Preview" />
            </div>
          )}
          <button onClick={handleSubmit}>Generate Caption</button>
        </section>

        {error && <div className="error">{error}</div>}

        <section className="output-section">
          <h2>Generated Caption for the Image</h2>
          <p>{caption}</p>

          <h2>Braille Representation of the Summary</h2>
          <p>{braille}</p>
        </section>
      </main>

      </div>
  );
}

export default App;
