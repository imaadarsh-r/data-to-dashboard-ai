import { useState } from 'react';
import PropTypes from 'prop-types';

function JsonInput({ value, onChange }) {
    const [isValid, setIsValid] = useState(true);
    const [isDragging, setIsDragging] = useState(false);

    const handleChange = (e) => {
        const newValue = e.target.value;
        onChange(newValue);

        // Validate JSON
        if (newValue.trim()) {
            try {
                JSON.parse(newValue);
                setIsValid(true);
            } catch {
                setIsValid(false);
            }
        } else {
            setIsValid(true);
        }
    };

    const handleFileUpload = (file) => {
        if (file && file.type === 'application/json') {
            const reader = new FileReader();
            reader.onload = (e) => {
                const content = e.target.result;
                onChange(content);

                // Validate the uploaded JSON
                try {
                    JSON.parse(content);
                    setIsValid(true);
                } catch {
                    setIsValid(false);
                }
            };
            reader.readAsText(file);
        } else {
            alert('Please upload a valid JSON file (.json)');
        }
    };

    const handleFileInputChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer.files[0];
        if (file) {
            handleFileUpload(file);
        }
    };

    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">
                    <span className="card-icon">📝</span>
                    JSON Data
                </h2>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    {value && (
                        <span style={{
                            fontSize: '0.75rem',
                            color: isValid ? 'var(--success)' : 'var(--error)',
                            fontWeight: 600
                        }}>
                            {isValid ? '✓ Valid JSON' : '✗ Invalid JSON'}
                        </span>
                    )}
                    <label
                        htmlFor="json-file-upload"
                        className="btn btn-secondary"
                        style={{
                            fontSize: '0.875rem',
                            padding: '0.5rem 1rem',
                            cursor: 'pointer',
                            margin: 0
                        }}
                    >
                        <span className="btn-icon">📁</span>
                        Upload JSON
                    </label>
                    <input
                        id="json-file-upload"
                        type="file"
                        accept=".json,application/json"
                        onChange={handleFileInputChange}
                        style={{ display: 'none' }}
                    />
                </div>
            </div>
            <div className="input-group">
                <label className="label">
                    Paste your JSON data here or drag & drop a JSON file
                </label>
                <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    style={{
                        position: 'relative',
                        border: isDragging ? '2px dashed var(--accent-primary)' : 'none',
                        borderRadius: 'var(--radius-md)',
                        transition: 'all 0.2s ease'
                    }}
                >
                    <textarea
                        className="textarea"
                        value={value}
                        onChange={handleChange}
                        placeholder={`{\n  "report_title": "My Dashboard",\n  "data": [...]\n}`}
                        spellCheck="false"
                    />
                    {isDragging && (
                        <div style={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            background: 'rgba(99, 102, 241, 0.1)',
                            borderRadius: 'var(--radius-md)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            pointerEvents: 'none'
                        }}>
                            <div style={{
                                fontSize: '1.5rem',
                                color: 'var(--accent-primary)',
                                fontWeight: 600
                            }}>
                                📁 Drop JSON file here
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

JsonInput.propTypes = {
    value: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
};

export default JsonInput;
