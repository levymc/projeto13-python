import axios from 'axios'

// axios.get('http://localhost:5000/participants').then(res => {
//     console.log(res.data)
// }).catch(err => {
//     console.log(err)
// })

axios.get('http://192.168.15.98:5000/messages?limit=100', {headers: {User: "Levy"}}).then(res => {
    console.log(res.data)
}).catch(err => {
    console.log(err)
})
