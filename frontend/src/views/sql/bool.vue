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
  name: 'BoolTest',
  data () {
    return {
      getDBName: (data) => post(`/api/bool/GetDBName`, data),
      getDBTables: (data) => post(`/api/bool/GetDBTables`, data),
      getDBColumns: (data) => post(`/api/bool/GetDBColumns`, data),
      getDBData: (data) => post(`/api/bool/GetDBData`, data)
    }
  },
  components: {
    BasicComponent
  }
}
</script>
