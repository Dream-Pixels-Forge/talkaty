const wave = document.querySelector('#hero-wave');
if (wave) {
  const levels = [8, 15, 25, 18, 32, 48, 28, 42, 56, 34, 21, 38, 54, 26, 47, 62, 37, 53, 31, 44, 22, 36, 49, 25, 40, 56, 33, 45, 27, 38, 18, 29, 43, 23, 34, 16, 27, 12];
  wave.innerHTML = levels.map((height, index) => `<span class="wave-bar" style="--h:${height}px;--delay:${(index % 8) * -0.13}s"></span>`).join('');
}

const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#primary-nav');
if (menuButton && nav) {
  menuButton.addEventListener('click', () => {
    const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!isOpen));
    menuButton.setAttribute('aria-label', isOpen ? 'Open navigation' : 'Close navigation');
    nav.classList.toggle('is-open', !isOpen);
  });
  nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Open navigation');
    nav.classList.remove('is-open');
  }));
}

document.querySelectorAll('[data-copy]').forEach((button) => {
  const initialLabel = button.querySelector('.copy-label')?.textContent || 'Copy';
  button.addEventListener('click', async () => {
    const text = button.dataset.copy || '';
    const status = document.querySelector('#copy-status');
    try {
      await navigator.clipboard.writeText(text);
      button.classList.add('is-copied');
      button.querySelector('.copy-label').textContent = 'Copied';
      if (status) status.textContent = 'Command copied — ready for your terminal.';
      window.setTimeout(() => {
        button.classList.remove('is-copied');
        button.querySelector('.copy-label').textContent = initialLabel;
      }, 1800);
    } catch {
      if (status) status.textContent = `Select and copy this command: ${text}`;
    }
  });
});
