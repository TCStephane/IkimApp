
-- MEMBERS TABLE
CREATE TABLE IF NOT EXISTS members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    member_name VARCHAR(255) NOT NULL,
    date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(13) NOT NULL UNIQUE,
    physical_address TEXT
);

-- CYCLES TABLE
CREATE TABLE IF NOT EXISTS cycles (
    cycle_id INT AUTO_INCREMENT PRIMARY KEY,
    cycle_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- TRANSACTIONS TABLE
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    transaction_type ENUM('savings', 'loan_repayment', 'interest') NOT NULL,
    tx_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_transactions_member
        FOREIGN KEY (member_id)
        REFERENCES members(member_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- CYCLE_BENEFICIARIES TABLE
CREATE TABLE IF NOT EXISTS cycle_beneficiaries (
    cycle_benef_id INT AUTO_INCREMENT PRIMARY KEY,
    cycle_id INT NOT NULL,
    member_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    received_funds TINYINT(1) DEFAULT 0,
    received_date DATE,

    CONSTRAINT fk_cyclebenef_cycle
        FOREIGN KEY (cycle_id)
        REFERENCES cycles(cycle_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_cyclebenef_member
        FOREIGN KEY (member_id)
        REFERENCES members(member_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
