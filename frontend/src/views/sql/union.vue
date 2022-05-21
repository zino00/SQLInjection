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
  name: 'UnionTest',
  data () {
    return {
      getDBName: (data) => post(`/api/union/GetDBName`, data),
      getDBTables: (data) => post(`/api/union/GetDBTables`, data),
      getDBColumns: (data) => post(`/api/union/GetDBColumns`, data),
      getDBData: (data) => post(`/api/union/GetDBData`, data)
    }
  },
  components: {
    BasicComponent
  }
}
</script>
