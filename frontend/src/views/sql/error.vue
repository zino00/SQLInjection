<template>
  <keep-alive>
    <BasicComponent
      :getDBName="getDBName"
      :getDBTables="getDBTables"
      :getDBColumns="getDBColumns"
      :getDBData="getDBData"
    ></BasicComponent>
  </keep-alive>
</template>

<script language="ts">
import { post } from '@/utils/request'
import BasicComponent from '@/views/sql/basic.vue'

export default {
  name: 'ErrorTest',
  data () {
    return {
      getDBName: (data) => post(`/api/error/GetDBName`, data),
      getDBTables: (data) => post(`/api/error/GetDBTables`, data),
      getDBColumns: (data) => post(`/api/error/GetDBColumns`, data),
      getDBData: (data) => post(`/api/error/GetDBData`, data)
    }
  },
  components: {
    BasicComponent
  }
}
</script>
