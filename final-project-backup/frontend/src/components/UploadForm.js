import React, { useState } from 'react';
import axios from 'axios';

function UploadForm({ setResult }) {
  const [task, setTask] = useState('feedback');
  const [content, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('task', task);
    formData.append('content', content);

    const response = await axios.post('http://127.0.0.1:8000/analyze/', formData);
    setResult(response.data.result);
  };

  return (
    <form onSubmit={handleSubmit}>
      <select value={task} onChange={(e) => setTask(e.target.value)}>
        <option value="create">Create Material</option>
        <option value="feedback">Provide Feedback</option>
        <option value="grade">Grade Document</option>
      </select>
      <br />
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Paste or type document content here"
        rows="10"
        cols="50"
      />
      <br />
      <button type="submit">Submit</button>
    </form>
  );
}

export default UploadForm;
