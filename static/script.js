const form = document.getElementById('coach-form');
const submitBtn = document.getElementById('submit-btn');

const outputEmpty = document.getElementById('output-empty');
const outputResult = document.getElementById('output-result');
const outputError = document.getElementById('output-error');

const techniqueBadge = document.getElementById('technique-badge');
const promptBox = document.getElementById('prompt-box');
const togglePromptBtn = document.getElementById('toggle-prompt');
const planText = document.getElementById('plan-text');

const TECHNIQUE_LABELS = {
  zero_shot: 'Zero-shot',
  few_shot: 'Few-shot',
  structured: 'Structured reasoning',
};

togglePromptBtn.addEventListener('click', () => {
  const isHidden = promptBox.hasAttribute('hidden');
  if (isHidden) {
    promptBox.removeAttribute('hidden');
    togglePromptBtn.textContent = 'Hide prompt sent';
  } else {
    promptBox.setAttribute('hidden', '');
    togglePromptBtn.textContent = 'View prompt sent';
  }
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const payload = {
    name: formData.get('name').trim(),
    subject: formData.get('subject').trim(),
    weak_topics: formData.get('weak_topics').trim(),
    days_remaining: Number(formData.get('days_remaining')),
    hours_per_day: Number(formData.get('hours_per_day')),
    skill_level: formData.get('skill_level'),
    technique: formData.get('technique'),
  };

  setLoading(true);
  hideAll();

  try {
    const res = await fetch('/api/generate-plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (data.error) {
      showError(data.error, data.prompt_used);
    } else {
      showResult(data);
    }
  } catch (err) {
    showError('Could not reach the server. Is the FastAPI app running?');
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.textContent = isLoading ? 'Asking Gemini…' : 'Generate study plan';
}

function hideAll() {
  outputEmpty.setAttribute('hidden', '');
  outputResult.setAttribute('hidden', '');
  outputError.setAttribute('hidden', '');
}

function showResult(data) {
  techniqueBadge.textContent = TECHNIQUE_LABELS[data.technique] || data.technique;
  promptBox.textContent = data.prompt_used || '';
  promptBox.setAttribute('hidden', '');
  togglePromptBtn.textContent = 'View prompt sent';
  planText.textContent = data.response || '';
  outputResult.removeAttribute('hidden');
}

function showError(message, promptUsed) {
  let text = message;
  if (promptUsed) {
    text += '\n\nThe prompt that would have been sent:\n' + promptUsed;
  }
  outputError.textContent = text;
  outputError.style.whiteSpace = 'pre-wrap';
  outputError.removeAttribute('hidden');
}
