import vSelect from 'vue-select'

// @ts-ignore
vSelect.props.components.default = () => ({
  Deselect: {
    render: (h: any) =>
      h('vue-feather', { props: { size: '15', type: 'x' } })
  },
  OpenIndicator: {
    render: (h: any) =>
      h('vue-feather', {
        props: { size: '15', type: 'chevron-down' },
        class: 'open-indicator'
      })
  }
})

export default vSelect
