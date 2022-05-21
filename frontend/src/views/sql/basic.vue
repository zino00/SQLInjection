<template>
  <div class="app-container">
    <el-form :model="queryData" ref="queryForm" :inline="true">
      <el-form-item label="目标 URL：">
        <el-input v-model="queryData.url"></el-input>
      </el-form-item>

      <el-form-item label="数据库名称：">
        <el-input v-model="queryData.DBName"></el-input>
      </el-form-item>

      <el-form-item label="数据表名：">
        <el-select v-model="queryData.DBTable" @change="changeDBTableSelected($event)">
          <el-option
            v-for="(item,id) in testTableData" :key="id"
            :label="item.tableName"
            :value="item.tableName"
          >
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="数据库列名：">
          <el-select v-model="queryData.DBColumns">
            <el-option
              v-for="(item,id) in selectedColumns" :key="id"
              :label="item.columnName"
              :value="item.columnName"
            >
            </el-option>
          </el-select>
      </el-form-item>
      <div>
        <el-form-item>
          <el-button type="primary" @click="queryDBName">查询数据库名称</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="queryDBTable">查询数据库表名</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="queryDBColumn">查询数据库列名</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="queryDBData">查询数据库列值</el-button>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="clearAll">清除全部信息</el-button>
        </el-form-item>
      </div>

      <div>
        <el-table :data="testTableData" style="width: 100%" v-loading="listLoading">

          <el-table-column prop="childs" type="expand">
            <template slot-scope="scope">
              <el-table :data="scope.row.childs" style="width: 100%">
                <el-table-column
                  v-for="(item, index) in scope.row.columns"
                  :key="index"
                  :prop="item.columnName"
                  :label="item.columnName"
                  align="center"
                  min-width="250px"
                >
                </el-table-column>
              </el-table>
            </template>
          </el-table-column>

          <el-table-column prop="tableName" label="表名">
          </el-table-column>
        </el-table>
      </div>
    </el-form>
  </div>
</template>

<script language="ts">
export default {
  name: 'BasicComponent',
  props: {
    getDBName: {
      type: Function,
      required: true
    },
    getDBTables: {
      type: Function,
      required: true
    },
    getDBColumns: {
      type: Function,
      required: true
    },
    getDBData: {
      type: Function,
      required: true
    }
  },
  data () {
    return {
      queryData: {
        url: '',
        DBName: '',
        DBTable: '',
        DBColumns: ''
      },
      selectedColumns: [],

      listLoading: false,
      testTableData: [
        {
          tableName: 'tbname1',
          columns: [
            { columnName: 'column11' },
            { columnName: 'column12' },
            { columnName: 'column13' },
            { columnName: 'column14' },
            { columnName: 'column15' }
          ],
          childs: [
            {
              column11: '1data11',
              column12: '1data21',
              column13: '1data31',
              column14: '1data41',
              column15: '1data51'
            },
            {
              column11: '1data12',
              column12: '1data22',
              column13: '1data32',
              column14: '1data42',
              column15: '1data52'
            },
            {
              column11: '1data13',
              column12: '1data23',
              column13: '1data33',
              column14: '1data43',
              column15: '1data53'
            }
          ]
        },
        {
          tableName: 'tbname2',
          columns: [
            { columnName: 'column21' },
            { columnName: 'column22' },
            { columnName: 'column23' }
          ],
          childs: [
            {
              column21: '2data11',
              column22: '2data21',
              column23: '2data31'
            },
            {
              column21: '2data12',
              column22: '2data22',
              column23: '2data32'
            },
            {
              column21: '2data13',
              column22: '2data23',
              column23: '2data33'
            }
          ]
        }
      ]
    }
  },
  methods: {
    changeDBTableSelected (value) {
      this.queryData.DBColumns = ''
      this.selectedColumns = []

      let _this = this
      this.testTableData.forEach((item) => {
        if (item.tableName === value) {
          _this.selectedColumns = item.columns
        }
      })
    },
    clearAll () {
      this.testTableData = []
      this.selectedColumns = []
      this.queryData.DBTable = this.queryData.DBColumns = ''
    },
    queryDBName () {
      if (this.queryData.url === '') {
        this.$message.error('请输入数据库 URL')
        return
      }

      this.listLoading = true
      this.getDBName(this.queryData).then(data => {
        let dbname = data.DBName

        // check
        let jsontext = JSON.stringify(dbname)
        if (jsontext === undefined || jsontext === '') {
          this.$message.error('爆破失败，后端数据返回为空')
        }

        this.$message.success('爆破成功，数据库名称为 ' + dbname)
        this.queryData.DBName = dbname
        this.listLoading = false
      }).catch((error) => {
        var msg = '爆破失败' + (error.response ? ': ' + error.response.statusText : '');
        this.$message.error(msg)
        this.listLoading = false
      })
    },
    queryDBTable () {
      if (this.queryData.url === '') {
        this.$message.error('请输入数据库 URL')
        return
      } else if (this.queryData.DBName === '') {
        this.$message.error('请输入数据库名称')
        return
      }

      this.listLoading = true
      this.getDBTables(this.queryData).then(data => {
        let DBTables = data.DBTables

        // check
        let jsontext = JSON.stringify(DBTables)
        if (jsontext === undefined || jsontext === '{}' || jsontext === '[]') {
          this.$message.error('爆破失败，后端数据返回为空')
        }

        for (var key in DBTables) {
          let found = false
          this.testTableData.forEach((item) => {
            if (item.tableName === DBTables[key]) {
              found = true
            }
          })
          if (!found) {
            this.testTableData.append({ tableName: DBTables[key] })
          }
        }

        this.$message.success('爆破成功')
        this.listLoading = false
      }).catch((error) => {
        var msg = '爆破失败' + (error.response ? ': ' + error.response.statusText : '');
        this.$message.error(msg)
        this.listLoading = false
      })
    },
    queryDBColumn () {
      if (this.queryData.url === '') {
        this.$message.error('请输入数据库 URL')
        return
      } else if (this.queryData.DBName === '') {
        this.$message.error('请输入数据库名称')
        return
      } else if (this.queryData.DBTable === '') {
        this.$message.error('请输入数据表名称')
        return
      }

      this.listLoading = true
      this.getDBColumns(this.queryData).then(data => {
        let DBColumns = data.DBColumns

        // check
        let jsontext = JSON.stringify(DBColumns)
        if (jsontext === undefined || jsontext === '{}' || jsontext === '[]') {
          this.$message.error('爆破失败，后端数据返回为空')
        }

        let idx = 0
        for (idx = 0; idx < this.testTableData.length; idx++) {
          if (this.testTableData[idx].tableName === this.queryData.DBTable) {
            break
          }
        }
        if (this.testTableData[idx].columns === undefined) {
          this.testTableData[idx].columns = []
          for (let column in DBColumns) {
            this.testTableData[idx].columns.push(column)
          }
        }

        this.$message.success('爆破成功')
        this.listLoading = false
      }).catch((error) => {
        var msg = '爆破失败' + (error.response ? ': ' + error.response.statusText : '');
        this.$message.error(msg)
        this.listLoading = false
      })
    },
    queryDBData () {
      if (this.queryData.url === '') {
        this.$message.error('请输入数据库 URL')
        return
      } else if (this.queryData.DBName === '') {
        this.$message.error('请输入数据库名称')
        return
      } else if (this.queryData.DBTable === '') {
        this.$message.error('请输入数据表名称')
        return
      } else if (this.queryData.DBColumns === '') {
        this.$message.error('请输入数据列名称')
        return
      }

      this.listLoading = true
      this.getDBData(this.queryData).then(data => {
        let DBData = data.DBData

        // check
        let jsontext = JSON.stringify(DBData)
        if (jsontext === undefined || jsontext === '{}' || jsontext === '[]') {
          this.$message.error('爆破失败，后端数据返回为空')
        }

        let idx = 0
        for (idx = 0; idx < this.testTableData.length; idx++) {
          if (this.testTableData[idx].tableName === this.queryData.DBTable) {
            break
          }
        }
        for (var key in DBData) {
          let datalist = DBData[key]
          for (let i = 0; i < datalist.arr; i++) {
            if (this.testTableData[idx].childs === undefined) {
              this.testTableData[idx].childs = []
            } else if (this.testTableData[idx].childs[i] === undefined) {
              this.testTableData[idx].childs[i] = {}
            } else {
              this.testTableData[idx].childs[i].key = datalist[i]
            }
          }
        }

        this.$message.success('爆破成功')
        this.listLoading = false
      }).catch((error) => {
        var msg = '爆破失败' + (error.response ? ': ' + error.response.statusText : '');
        this.$message.error(msg)
        this.listLoading = false
      })
    }
  }
}
</script>
