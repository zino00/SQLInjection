<template>
  <BasicComponent
    :getDBName="getDBName"
    :getDBTables="getDBTables"
    :getDBColumns="getDBColumns"
    :getDBData="getDBData"
  ></BasicComponent>
</template>

<script language="ts">
import { post } from '@/utils/request'
import BasicComponent from '@/views/sql/basic.vue'

export default {
  data () {
    let type = 'union'
    return {
      getDBName: (data) => post(`/api/${type}/GetDBName`, data),
      getDBTables: (data) => post(`/api/${type}/GetDBTables`, data),
      getDBColumns: (data) => post(`/api/${type}/GetDBColumns`, data),
      getDBData: (data) => post(`/api/${type}/GetDBData`, data)
    }
  },
  components: {
    BasicComponent
  }
}
</script>
