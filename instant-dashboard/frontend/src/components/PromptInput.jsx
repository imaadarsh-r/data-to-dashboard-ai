import PropTypes from 'prop-types';

function PromptInput({ value, onChange }) {
    const charCount = value.length;
    const maxChars = 500;

    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">
                    <span className="card-icon">💬</span>
                    Design Instructions
                </h2>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    {charCount}/{maxChars}
                </span>
            </div>
            <div className="input-group">
                <label className="label">
                    Describe how you want your dashboard to look
                </label>
                <textarea
                    className="textarea"
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    placeholder="Example: Design a sleek analytics dashboard with a dark theme. Display key metrics as glowing cards with gradient borders. Use vibrant colors and modern styling..."
                    maxLength={maxChars}
                    style={{ minHeight: '300px' }}
                />
            </div>
            <div style={{
                fontSize: '0.75rem',
                color: 'var(--text-muted)',
                marginTop: 'var(--spacing-sm)'
            }}>
                💡 Tip: Be specific about colors, layout, and style preferences
            </div>
        </div>
    );
}

PromptInput.propTypes = {
    value: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
};

export default PromptInput;
