import PropTypes from 'prop-types';

function GenerateButton({ onClick, isLoading, disabled }) {
    return (
        <button
            className="btn btn-primary generate-btn"
            onClick={onClick}
            disabled={disabled || isLoading}
        >
            {isLoading ? (
                <>
                    <div className="spinner" />
                    Generating Dashboard...
                </>
            ) : (
                <>
                    <span className="btn-icon">✨</span>
                    Generate Dashboard
                </>
            )}
        </button>
    );
}

GenerateButton.propTypes = {
    onClick: PropTypes.func.isRequired,
    isLoading: PropTypes.bool.isRequired,
    disabled: PropTypes.bool,
};

export default GenerateButton;
