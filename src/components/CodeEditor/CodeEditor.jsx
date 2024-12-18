import React, { useState } from 'react';
import axios from 'axios';
import { Editor } from '@monaco-editor/react';
import styles from './style.module.css';
import { SelectLanguage } from '../SelectLanguage/SelectLanguage';

   export const CodeEditor = () => {
     const [code, setCode] = useState('// Введите Ваш код');
     const [output, setOutput] = useState('');
     const [language, setLanguage] = useState(undefined);

     const handleEditorChange = (value) => {
       setCode(value);
     };

     const runCode = async () => {
      const newCode = code.trim()
      if(language === undefined){
        setOutput('Выберите язык программирования');
      }else if(language === 'php' && (!newCode.startsWith("<?php") || !newCode.endsWith("?>"))){
        setOutput('Проверьте открывающий (<?php) и закрывающий (?>) теги');
      }
      else{   
        try {
          const response = await axios.post(`http://127.0.0.1:8000/execute/${language}`, {
              "code": newCode
          }, {
            headers: {
                'Content-Type': 'application/json',
            }
          });
          if (response.data.returncode === 0){
            setOutput(response.data.stdout);
          } else {
            setOutput(response.data.stderr);
          }
          
        } catch (error) {
          setOutput(`Ошибка: ${error}`);
        }
        }

    };

     return (
      <>
        <SelectLanguage onLanguage={setLanguage}/>
        <div className={styles.codeEditor}>
          <div className={styles.editor}>
            <Editor
              height="100%"
              width="100%"
              className={styles.custom_editor}
              language={language}
              value={code}
              onChange={handleEditorChange}
              options={{
                selectOnLineNumbers: true,
              }}
            />
          </div>

          <button onClick={runCode} className={styles.button}>Run</button>
          <div>
            <h3>Результат:</h3>
            <pre>{output}</pre>
          </div>
     
        </div>
      </>
 
      
     );
   };
