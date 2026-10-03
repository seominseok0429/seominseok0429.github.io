document.querySelectorAll('[data-comparison]').forEach(figure => {
  const stage = figure.querySelector('.comparison-stage');
  const input = figure.querySelector('input[type="range"]');
  const controls = figure.querySelector('.comparison-controls');
  const update = value => {
    const position = Math.max(0, Math.min(100, Math.round(value)));
    input.value = position;
    input.setAttribute('aria-valuetext', `원본 ${position}%, 변환 ${100 - position}%`);
    stage.style.setProperty('--position', `${position}%`);
  };
  figure.classList.add('is-interactive');
  controls.hidden = false;
  update(input.value);
  input.addEventListener('input', () => update(input.value));
  const move = event => {
    const rect = stage.getBoundingClientRect();
    update((event.clientX - rect.left) / rect.width * 100);
  };
  // Native image dragging otherwise interrupts pointer movement in browsers.
  stage.querySelectorAll('img').forEach(image => { image.draggable = false; });
  stage.addEventListener('dragstart', event => event.preventDefault());
  stage.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse') move(event);
  });
  stage.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    stage.setPointerCapture(event.pointerId);
    input.focus({ preventScroll: true });
    move(event);
  });
  stage.addEventListener('pointermove', event => {
    if (event.pointerType === 'mouse' || stage.hasPointerCapture(event.pointerId)) move(event);
  });
  const release = event => {
    if (stage.hasPointerCapture(event.pointerId)) stage.releasePointerCapture(event.pointerId);
  };
  stage.addEventListener('pointerup', release);
  stage.addEventListener('pointercancel', release);
});
