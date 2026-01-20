import { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';

function DashboardPreview({ htmlContent, isLoading }) {
    const iframeRef = useRef(null);

    useEffect(() => {
        if (htmlContent && iframeRef.current) {
            const iframe = iframeRef.current;
            const doc = iframe.contentDocument || iframe.contentWindow.document;
            doc.open();
            doc.write(htmlContent);
            doc.close();
        }
    }, [htmlContent]);

    const handleDownload = () => {
        if (!htmlContent) return;

        // Create a blob from the HTML content
        const blob = new Blob([htmlContent], { type: 'text/html' });
        const url = URL.createObjectURL(blob);

        // Create a temporary link and trigger download
        const link = document.createElement('a');
        link.href = url;
        link.download = `dashboard_${new Date().getTime()}.html`;
        document.body.appendChild(link);
        link.click();

        // Cleanup
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };

    const handleCopyCode = () => {
        if (!htmlContent) return;

        navigator.clipboard.writeText(htmlContent).then(() => {
            alert('✓ HTML code copied to clipboard!');
        }).catch(() => {
            alert('Failed to copy code. Please try again.');
        });
    };

    return (
        <div className="preview-container">
            <div className="preview-header">
                <h2 className="preview-title">
                    <span className="card-icon">🎨</span>
                    Dashboard Preview
                </h2>
                {htmlContent && !isLoading && (
                    <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
                        <button
                            className="btn btn-secondary"
                            onClick={handleCopyCode}
                            style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                        >
                            <span className="btn-icon">📋</span>
                            Copy Code
                        </button>
                        <button
                            className="btn btn-primary"
                            onClick={handleDownload}
                            style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                        >
                            <span className="btn-icon">⬇️</span>
                            Download HTML
                        </button>
                    </div>
                )}
            </div>

            <div className="preview-content">
                {isLoading ? (
                    <div className="loading-state">
                        <div className="loading-spinner" />
                        <div className="loading-text">
                            Generating your beautiful dashboard...
                        </div>
                    </div>
                ) : htmlContent ? (
                    <iframe
                        ref={iframeRef}
                        className="preview-iframe"
                        title="Dashboard Preview"
                        sandbox="allow-same-origin"
                    />
                ) : (
                    <div className="empty-state">
                        <div className="empty-icon">📊</div>
                        <div className="empty-title">No Dashboard Yet</div>
                        <div className="empty-description">
                            Enter your JSON data and design instructions above, then click "Generate Dashboard" to see your custom dashboard appear here.
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

DashboardPreview.propTypes = {
    htmlContent: PropTypes.string,
    isLoading: PropTypes.bool.isRequired,
};

export default DashboardPreview;
