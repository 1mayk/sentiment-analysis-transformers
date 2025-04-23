import React, { useState } from "react";
import { analyze, batch } from "./api";
import { trainModel } from "./train";

export default function App() {
  const [text, setText] = useState("");
  const [res, setRes] = useState("");
  const [file, setFile] = useState(null),
    [out, setOut] = useState("");
  const [trainFile, setTrainFile] = useState(null),
    [trainRes, setTrainRes] = useState("");

  return (
    <div className="p-4">
      <h2>Análise Única</h2>
      <textarea value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={async () => setRes((await analyze(text)).sentiment)}>
        Analisar
      </button>
      <p>{res}</p>

      <h2>Batch</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={async () => setOut((await batch(file)).file)}>
        Processar
      </button>
      <p>{out}</p>

      <h2>Treinamento</h2>
      <input type="file" onChange={(e) => setTrainFile(e.target.files[0])} />
      <button
        onClick={async () => setTrainRes((await trainModel(trainFile)).status)}
      >
        Treinar
      </button>
      <p>{trainRes}</p>
    </div>
  );
}
