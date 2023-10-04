search = document.getElementById('Search')
table11 = document.getElementById('table1')
table2 = document.getElementById('table2')
tableRows = document.getElementById('result-rows')
error = document.getElementById('no-result')
table2.style.display ="NONE"
search.addEventListener('keyup',(e)=>{
    searchVal =e.target.value;
    if(searchVal.length>0){
        table11.style.display ="NONE"
        table2.style.display ="BLOCK"
        tableRows.innerHTML=''
        fetch("/expenses/search_expenses/",{
            body : JSON.stringify({search:searchVal}) ,
            method : 'post'
        })
        .then(res => res.json())
        .then(data =>{
            if (data.length > 0) {
                error.innerHTML = ''
                data.forEach(expense => {
                    tableRows.innerHTML += ( `
                    <tr>
                    <td>${expense.amount}</td>
                    <td>${expense.description}</td>
                    <td>${expense.category}</td>
                    <td>${new Date(expense.date).toDateString()}</td>
                    <td>
                       <span><a href="edit-expense/${expense.id}"><i class="fas fa-edit" style="color: darkgreen;" >  </i></a></span>
                    </td>
                    <td>
                        <span> <a href=""delete-expense/${expense.id}""><i class="fas fa-trash" style="color: red;"> </i></a></span>
                    </td>
                    </tr>
                        `)
                });
              } else {
                error.innerHTML = `<p class="text-info lead">No Results Found</p>`;
                table2.style.display ="NONE"
              }
        })
        
    }
    else{
        table2.style.display ="NONE"
        table11.style.display ="block"
    }
    

});