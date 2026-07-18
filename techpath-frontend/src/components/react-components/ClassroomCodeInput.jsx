import { useRef } from 'react';

export default function ClassroomCodeInput({ value, onChange, onSubmit, disabled, error }) {
  const refs = useRef([]);
  const digits = value.padEnd(6, ' ').split('').slice(0, 6);

  const setDigit = (index, char) => {
    const next = digits.slice();
    next[index] = char;
    const joined = next.join('').replace(/ /g, '');
    onChange(joined);
    return joined;
  };

  const handleChange = (index, raw) => {
    const char = raw.replace(/[^0-9]/g, '').slice(-1);
    if (!char) return;
    const joined = setDigit(index, char);
    if (index < 5) refs.current[index + 1]?.focus();
    // Pass the freshly-assembled code straight through rather than letting onSubmit
    // re-read the parent's state: setDigit's onChange(joined) call above hasn't
    // flushed yet, so a parameterless onSubmit() fired synchronously in this same
    // handler would still see the pre-update (5-character) value and bail out.
    if (index === 5 && joined.length === 6) {
      onSubmit(joined);
    }
  };

  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace') {
      if (digits[index] !== ' ') {
        setDigit(index, ' ');
      } else if (index > 0) {
        setDigit(index - 1, ' ');
        refs.current[index - 1]?.focus();
      }
    } else if (e.key === 'ArrowLeft' && index > 0) {
      refs.current[index - 1]?.focus();
    } else if (e.key === 'ArrowRight' && index < 5) {
      refs.current[index + 1]?.focus();
    } else if (e.key === 'Enter') {
      onSubmit(value);
    }
  };

  const handlePaste = (e) => {
    const text = e.clipboardData.getData('text').replace(/[^0-9]/g, '').slice(0, 6);
    if (!text) return;
    e.preventDefault();
    onChange(text);
    if (text.length === 6) {
      refs.current[5]?.focus();
      onSubmit(text);
    } else {
      refs.current[text.length]?.focus();
    }
  };

  return (
    <div>
      <div className="flex justify-center gap-2 sm:gap-3" onPaste={handlePaste}>
        {digits.map((d, i) => (
          <input
            key={i}
            ref={(el) => (refs.current[i] = el)}
            type="text"
            inputMode="numeric"
            maxLength={1}
            disabled={disabled}
            value={d === ' ' ? '' : d}
            onChange={(e) => handleChange(i, e.target.value)}
            onKeyDown={(e) => handleKeyDown(i, e)}
            onFocus={(e) => e.target.select()}
            className={`h-14 w-11 rounded-xl border bg-slate-900 text-center font-mono text-2xl font-bold text-white outline-none transition sm:h-16 sm:w-14 ${
              error
                ? 'border-red-500 ring-2 ring-red-500/30'
                : 'border-slate-700 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/30'
            } disabled:opacity-50`}
          />
        ))}
      </div>
      {error && <p className="mt-3 text-center text-sm text-red-400">{error}</p>}
    </div>
  );
}
