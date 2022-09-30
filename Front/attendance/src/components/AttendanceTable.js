import React, { useState, useEffect } from 'react';
import PropTypes from "prop-types";
import axios from "axios";
import { Typography } from "@mui/material";
import MaterialTable from "material-table";
import GetAppIcon from "@material-ui/icons/GetApp";
import PlayCircleOutlineRoundedIcon from "@mui/icons-material/PlayCircleOutlineRounded";
import AddIcon from "@material-ui/icons/Add";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
import tableIcons from "../TableIcons"



function AttendanceTable() {
    const [attendanceData, setAttendanceData] = useState([])
    useEffect(() => {
        let attData = [] ; 
        axios.get(`http://localhost:5000/`)
        .then(async res => {
          const data = res.data;
          console.log('data',data);
          await data.forEach(element => {
          const values = element[0].split(',');
          attData.push({ studentName: values[0], attTime: values[1], lecTime: values[2], attPercentTime: values[3] ,moreThen70perc: values[4]})
          });
          console.log('attData',attData);
          setAttendanceData(attData) 
        })
    },[]);
    
    
    return (
    <div>
            <MaterialTable
              icons={tableIcons}
              title="Attendance In DevOps8200"
              columns={[
                { title: 'Student Name', field: 'studentName',
                cellStyle: {
                    backgroundColor: '#039be5',
                    color: '#FFF'
                  },
                  headerStyle: {
                    backgroundColor: '#039be5',
                  }},
                { title: 'Atendance time (min)', field: 'attTime' ,type: 'numeric' },
                { title: 'Lecture time (min)', field: 'lecTime', type: 'numeric' },
                { title: '% Attendance time', field: 'attPercentTime', type: 'numeric' },
                {
                    title: "More Then 70 %",
                    field: "moreThen70perc",
                    lookup: {"    YES":"    YES","    NO":"    NO"}
                },
              ]}
              data={attendanceData}        
              options={{
                filtering: true,
                exportButton: true,
                sorting: true,
                headerStyle: {
                    backgroundColor: '#01579b',
                    color: '#FFF'
                  }
              }}
            /></div>
          )
        }
        
  
  
  export default AttendanceTable;


