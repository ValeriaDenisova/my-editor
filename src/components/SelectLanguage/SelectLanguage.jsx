import React from 'react';
import { Select } from 'antd';
import styles from './style.module.css';

const { Option } = Select;

export const SelectLanguage = ({ onLanguage }) => {

 const handleChange = (value) => {
    onLanguage(value);
  };


  return (
    <div className={styles.selectLanguage}>
      <span>Выберите язык:</span>

      <Select
        defaultValue="выберите язык прграммирования"
        className={styles.select}
        style={{ width: '40%' }}
        onChange={handleChange}
      >
        <Option value="python">Python</Option>
        <Option value="php">PHP</Option>
        <Option value="javascript">JavaScript</Option>
      </Select>

    </div>
  );
};