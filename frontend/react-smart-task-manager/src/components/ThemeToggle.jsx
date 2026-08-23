function ThemeToggle({ theme, onToggleTheme }) {
  const isDark = theme === 'dark';

  return (
    <button className="theme-toggle" type="button" onClick={onToggleTheme} aria-label="Toggle light and dark theme">
      <span>{isDark ? 'Dark' : 'Light'} Theme</span>
      <span aria-hidden="true">{isDark ? 'Moon' : 'Sun'}</span>
    </button>
  );
}

export default ThemeToggle;
