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
  name: 'TimeTest',
  data () {
    return {
      getDBName: (data) => post(`/api/time/GetDBName`, data),
      getDBTables: (data) => post(`/api/time/GetDBTables`, data),
      getDBColumns: (data) => post(`/api/time/GetDBColumns`, data),
      getDBData: (data) => post(`/api/time/GetDBData`, data)
    }
  },
  components: {
    BasicComponent
  }
}
</script>
